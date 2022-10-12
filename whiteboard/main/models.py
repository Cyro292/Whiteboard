import secrets
from django.dispatch import receiver
from django.db.models.signals import post_init, pre_save, post_save
from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django import forms

# Create your models here.
    
class UserProfileManager(BaseUserManager):
    def create_user(self, email, username=None, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')
        if username is None:
            username=email

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username=None, password=None):
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
 
class AnonymousUser(models.Model):
    username = models.CharField(max_length=64, blank=False, null=False)
    
    
    def __str__(self) -> str:
        return str(self.username)
    
class Board(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    password = models.CharField(max_length=64)
    creation_date = models.DateTimeField(default=datetime.now(), null=False)
    users = models.ManyToManyField(to=get_user_model(), related_name="boards", through="UserParticipation")
    anonymous_users = models.ManyToManyField(
            to=AnonymousUser, 
            related_name="boards",
            through="AnonymousParticipation"
            )
    
    @property
    def owner(self):
        return self.userparticipation_set.get(permission=Participation.OWNER).user
    
    def add_user(self, user, permission=None):
        
        if permission is None:
            permission = Participation.READER

        return UserParticipation.objects.create(
                board=self, 
                user=user, 
                permission=permission)        
    
    def get_all_users(self):
        return self.users.all()
    
    def remove_user(self, user):
        
        if self.get_permission(user) == Participation.OWNER:
            raise Exception("cant remove the owner")
        
        self.users.remove(user=user)
    
    def get_permission_label(self, user):
        return self.userparticipation_set.get(user=user).get_permission_display()
    
    def get_permission(self, user):

        return self.userparticipation_set.get(user=user).permission    
        
    def set_permission(self, user, permission):
        
        if permission in (Participation.READER, Participation.WRITER, Participation.ADMIN):
            
            self.userparticipation_set.get(user=user).permission = permission
                
        elif permission is Participation.OWNER:
            if self.users.get(permission=Participation.OWNER).exist():
                self.userparticipation_set.get(permission=Participation.OWNER).permission = Participation.ADMIN
        
            self.userparticipation_set.get(user=user).permission = Participation.OWNER
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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)
    
    class Meta:
        unique_together = [["user", "board"]]

class AnonymousParticipation(Participation):
    user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, blank=False, null=False)
    
    class Meta:
        unique_together = [["user", "board"]]
    