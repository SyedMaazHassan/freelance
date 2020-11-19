from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.contrib.auth.models import AbstractUser
# Create your models here.



class client(models.Model):
    # additional fields
    fullName    = models.CharField(max_length = 25)
    city        = models.CharField(max_length = 25)
    postcode    = models.CharField(max_length = 25)
    email       = models.CharField(max_length = 25)
    homeAddress = models.CharField(max_length = 50)
    kvkNumber   = models.CharField(max_length = 25)

class freelancer(models.Model):
    firstName   = models.CharField(max_length = 25)
    lastName    = models.CharField(max_length = 25)
    email       = models.CharField(max_length = 25)
    phone       = models.CharField(max_length = 25)
    city        = models.CharField(max_length = 25)
    homeAddress = models.CharField(max_length = 50)
    speciality  = models.TextField()
    postcode    = models.CharField(max_length = 25)
    level       = models.CharField(max_length = 25)


class User(AbstractUser):
    ifClient = models.ForeignKey(client, on_delete = models.CASCADE, blank = True, null = True)
    ifFreelancer = models.ForeignKey(freelancer, on_delete = models.CASCADE, blank = True, null = True)