from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
    
class Client(models.Model):
        
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}"

class Board(models.Model):
    name = models.CharField(max_length=128)
    coworker: models.ManyToManyField = models.ManyToManyField(Client, related_name="boards", through='Participation')
    body = models.JSONField(null=True)
    
    def set_permission(self, client: Client, right):
        """Set the permission and right for a client in the board. 
        Cant set the Owner.

        Args:
            client (Client): _description_
            right (Participation.rights): _description_
        """
        
        if not self.coworker.contains(client):
            raise ObjectDoesNotExist
        
        participation: Participation = self.participation_set.get(client=client)
        
        if right == Participation.OWNER:
            #set the OWNER
            self.participation_set.get(right=Participation.OWNER).right = Participation.ADMIN
            participation.right = Participation.OWNER
            return
        
        if participation.right == Participation.OWNER:
            #the client is the owner
            raise Exception("cant remove the Owner")
        
        participation.right = right
        
    @property
    def owner(self):
        participation = self.participation_set.get(right=Participation.OWNER)
        return participation.client

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
    
    class Meta:
        unique_together = [['client', 'board']]
    
    def __str__(self) -> str:
        return f"{self.client} ({self.get_right_display()}) of {self.board}"
