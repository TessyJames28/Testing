from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Image, Group, User_Groups, Group_Events, Group_Image
from .serializers import (ImageSerializer,
                          GroupSerializer,
                          UserGroupsSerializer,
                          GroupEventsSerializer,
                          GroupImageSerializer)
from rest_framework.permissions import IsAuthenticated
from users.views import AuthenticationMiddleware

 

class ImageViewSet(AuthenticationMiddleware, viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class GroupViewSet(AuthenticationMiddleware, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # def create(self, request, *args, **kwargs):
    #     # Ensure the creator_id is set to the current user when creating a group.
    #     request.data['creator_id'] = request.user.id
    #     serializer = self.get_serializer(data=request.data)
        
    #     if serializer.is_valid():
    #         group = serializer.save()
            
    #         # Add the group creator to the User_Groups relationship
    #         group_owner = request.user
    #         group.usergroups_set.create(user=group_owner)
            
    #         return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGroupsViewSet(AuthenticationMiddleware, viewsets.ModelViewSet):
    queryset = User_Groups.objects.all()
    serializer_class = UserGroupsSerializer


class GroupEventsViewSet(AuthenticationMiddleware, viewsets.ModelViewSet):
    queryset = Group_Events.objects.all()
    serializer_class = GroupEventsSerializer


class GroupImageViewSet(AuthenticationMiddleware, viewsets.ModelViewSet):
    queryset = Group_Image.objects.all()
    serializer_class = GroupImageSerializer







