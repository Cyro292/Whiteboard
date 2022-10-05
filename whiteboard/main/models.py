import secrets
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')
        if username is None:
            username=email

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)
        Client.objects.create(user)

        return user

    def create_superuser(self, email, username, password):
        """ Create a new superuser profile """
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user
    
class CustomUser(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    
    
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Client(models.Model):
    
    user = models.OneToOneField(
        get_user_model(), 
        related_name="client", 
        blank=False, 
        null=False, 
        on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return str(self.user)
    
class AnonymousClient(models.Model):
    username = models.CharField(max_length=64, blank=False, null=False)
    session = models.CharField(max_length=225, blank=False, null=False)
    
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
    
    @property
    def owner(self):
        return self.userparticipation_set.get(permission=Participation.OWNER).client
    
    def add_client(self, client, permission=None):
        
        if permission is None:
            permission = Participation.READER

        return UserParticipation.objects.create(
                board=self, 
                client=client, 
                permission=permission)        
    
    def get_all_clients(self):
        return self.clients.all()
    
    def remove_client(self, client):
        
        if self.get_permission(client) == Participation.OWNER:
            raise Exception("cant remove the owner")
        
        self.clients.remove(client=client)
    
    def get_permission_label(self, client):
        return self.userparticipation_set.get(client=client).get_permission_display()
    
    def get_permission(self, client):

        return self.userparticipation_set.get(client=client).permission    
        
    def set_permission(self, client, permission):
        
        if permission in (Participation.READER, Participation.WRITER, Participation.ADMIN):
            
            self.userparticipation_set.get(client=client).permission = permission
                
        elif permission is Participation.OWNER:
            if self.clients.get(permission=Participation.OWNER).exist():
                self.userparticipation_set.get(permission=Participation.OWNER).permission = Participation.ADMIN
        
            self.userparticipation_set.get(client=client).permission = Participation.OWNER
        else:
            raise ValueError("unknown permission " + permission)
        
    def __str__(self) -> str:
        return f"{self.name}"
    
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
    