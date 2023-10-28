from django.db import models


class Account(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    email = models.CharField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150, blank=False, null=False)


class Company(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=150, blank=False, null=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)