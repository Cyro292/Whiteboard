from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
    
class Client(models.Model):
        
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return f"{self.user}"

class Board(models.Model):
    name = models.CharField(max_length=128)
    coworker = models.ManyToManyField(Client, related_name="boards", through='Participation')
    #TODO (JSON of all Objects in the Board)
    

    def __str__(self) -> str:
        return f"{self.name}"

class Participation(models.Model):  
    
    READER = 'R'
    WRITER = 'W'
    ADMIN = 'A'
    OWNER = 'O'
    
    rights = [
        (READER, 'Reader'),
        (WRITER, 'Writer'),
        (ADMIN, 'Admin'),
        (OWNER, 'Owner')
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    right = models.CharField(max_length=2, choices=rights)
    join_date = models.DateField()
    
    def __str__(self) -> str:
        return f"{self.client} ({self.get_right_display()}) of {self.board}"
