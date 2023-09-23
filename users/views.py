from django.shortcuts import render,redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.views import View
from .serializers import UserSerializer
from .models import User
from authlib.integrations.django_client import OAuth
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
import uuid
from rest_framework.views import APIView
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.core.cache import cache

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile',
    }
)

# Create your views here.
class AuthenticationMiddleware(APIView):
    serializer_class = UserSerializer  # Assuming the UserSerializer is already defined
    secret_key = settings.SECRET_KEY  # Replace with your actual secret key

    def check_authentication(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        token = authorization_header.split(' ')[1] if authorization_header.startswith('Bearer ') else ''

        if not token:
            failed_data = {
                "success": False,
                "status": 403,
                "message": "No token provided in the request header"
                }
            return JsonResponse(failed_data, status=403)

        serializer = URLSafeTimedSerializer(self.secret_key)
        user_id = serializer.loads(token, max_age=3600)  # Adjust expiration time if needed

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return user
            except User.DoesNotExist:
                pass

        failed_data = {
            "success": False,
            "status": 403,
            "message": "Invalid or expired token"
        }
        return JsonResponse(failed_data, status=403)

    def dispatch(self, request, *args, **kwargs):
        user = self.check_authentication(request)

        if not user:
            return HttpResponseForbidden()

        request.user = user
        return super().dispatch(request, *args, **kwargs)
    
    
# Create your views here.
class UserView(AuthenticationMiddleware, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class SingleUserView(AuthenticationMiddleware, generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    lookup_field = 'id'  # Set the lookup field to 'id'
    
    
class LoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse('auth'))
        return oauth.google.authorize_redirect(request, redirect_uri)

class AuthView(View):
    def get(self, request):
        token = oauth.google.authorize_access_token(request)

        User = get_user_model()
        email = token.get('userinfo', {}).get('email')
        name = token.get('userinfo', {}).get('name')
        picture = token.get('userinfo', {}).get('picture')
        access_token = token.get('access_token', {})
        id = token.get('userinfo', {}).get('sub')
        # access_token = token.get('access_token', {})
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email, id=str(id), name=name, avatar=picture)
        
        user, created = User.objects.get_or_create(email=email)
        user.access_token = access_token
        user.save()
        
        # Set the is_active status in Redis
        cache_key = f'user_active_status:{user.id}'
        cache.set(cache_key, True)

        # Generate a session token
        serializer = URLSafeTimedSerializer(AuthenticationMiddleware.secret_key)
        session_token = serializer.dumps(str(user.id))
        
        data = {
            "success": True,
            "user_id": id,
            "session_token": session_token,
            "status": 200
        }

        return JsonResponse(data)
