import uuid
from django.db import models
from django.contrib.auth.models import User




class Lobby(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(User ,on_delete=models.CASCADE, related_name="lobby_owner")
    title = models.CharField(max_length=30)


 
