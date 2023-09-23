from django.db import models
from users.models import User 
from events.models import Event, generateUUID


class Image(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False, default=generateUUID)
    url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False, default=generateUUID)
    title = models.CharField(max_length=225)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class User_Groups(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"User ID: {self.user_id}, Group ID: {self.group_id}"


class Group_Events(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Event ID: {self.event_id}, Group ID: {self.group_id}"
    
class Group_Image(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group Name: {self.group_id.title}, Image URL: {self.image_id.url}"
    