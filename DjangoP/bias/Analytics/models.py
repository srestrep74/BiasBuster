from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=150, blank=False, null=False)
    
    def __str__(self):
        return str(self.username)


#class Company(models.Model):
    #id = models.AutoField(primary_key=True, editable=False, unique=True)
    #name = models.CharField(max_length=150, blank=False, null=False)
    #account = models.ForeignKey(User_m, on_delete=models.CASCADE)