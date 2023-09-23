from rest_framework import serializers
from .models import Image, Group, User_Groups, Group_Events, Group_Image
from users.models import User
from events.models import Event


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserGroupsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = User_Groups
        fields = '__all__'


class GroupEventsSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = Group_Events
        fields = '__all__'


class GroupImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group_Image
        fields = '__all__'