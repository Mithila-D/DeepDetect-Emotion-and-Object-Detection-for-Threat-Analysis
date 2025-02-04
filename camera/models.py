from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    UserName = models.CharField(max_length=255, unique=True)
    Password = models.CharField(max_length=255) 

    def __str__(self):
        return self.UserName
