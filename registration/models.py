from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
# Create your models here.


class users(AbstractBaseUser):
    genders = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
    name = models.CharField(max_length=100)
    email = models.EmailField(primary_key=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=15, choices=genders)
    mobileno = models.CharField(max_length=10, unique=True)
    profilepic = models.ImageField(upload_to='profile_photos/')
    user_creation_date = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=25)
    is_authenticatedd = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'birthdate', 'gender', 'mobileno', 'password']
