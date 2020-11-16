from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=30)
    biometry = models.FileField()
    accessLevel = models.IntegerField()


