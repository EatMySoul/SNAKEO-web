from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=30)
    lobby = models.ForeignKey('Lobby', on_delete=models.CASCADE, blank=True)

class Lobby(models.Model):
    owner = models.OneToOneField('Player',on_delete=models.CASCADE, related_name="lobby_owner")
    title = models.CharField(max_length=30)



