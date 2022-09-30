import secrets
from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django import forms

# Create your models here.

class Client(models.Model):
    
    user = models.OneToOneField(get_user_model(), related_name="client", blank=False, null=False, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.user)
    
class AnonymousClient(models.Model):
    username = models.CharField(max_length=64, blank=False, null=False)
    
    def __str__(self) -> str:
        return str(self.username)
    
class Board(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    creation_date = models.DateTimeField(default=datetime.now(), null=False)
    clients = models.ManyToManyField(to=Client, related_name="boards", through="UserParticipation")
    anonymous_clients = models.ManyToManyField(
            to=AnonymousClient, 
            related_name="boards",
            through="AnonymousParticipation"
            )
    
    def add_client(self, client, permission=None):
        
        if permission is None:
            permission = Participation.READER
        
        if isinstance(client, Client):
            return UserParticipation.objects.create(
                    board=self, 
                    client=client, 
                    permission=permission)
        else:
            return AnonymousParticipation.objects.create(
                board=self, 
                client=client, 
                permission=permission)
    
    def get_permission_label(self, client):
        return self.userparticipation_set.get(client=client).get_permission_display()
    
    def get_permission(self, client):

        return self.userparticipation_set.get(client=client).permission    
        
    def set_permission(self, client, permission):
        
        if permission in (Participation.READER, Participation.WRITER, Participation.ADMIN):
            
            in_clients = self.clients.get(client).exist()
            
            if not in_clients:
                raise ObjectDoesNotExist("Not found")
            
            else:
                self.userparticipation_set.get(client=client).permission = permission
                
        elif permission is Participation.OWNER:
            if self.clients.get(permission=Participation.OWNER).exist():
                self.userparticipation_set.get(permission=Participation.OWNER).permission = Participation.ADMIN
        
            self.userparticipation_set.get(client=client).permission = Participation.OWNER
        else:
            raise ValueError("unknown permission " + permission)
    
class Participation(models.Model):
    OWNER = 1
    ADMIN = 2
    WRITER = 3
    READER = 4
    
    permissions = [
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (WRITER, "Writer"),
        (READER, "Reader"),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, blank=False, null=False)
    join_date = models.DateTimeField(default=datetime.now())
    permission = models.IntegerField(choices=permissions, default=READER, blank=False, null=False)
    
    class Meta:
        abstract = True
        
class UserParticipation(Participation):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    
    class Meta:
        unique_together = [["client", "board"]]

class AnonymousParticipation(Participation):
    client = models.ForeignKey(AnonymousClient, on_delete=models.CASCADE, blank=False, null=False)
    
    class Meta:
        unique_together = [["client", "board"]]
    