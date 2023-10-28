from django.db import models
from Analytics.models import *


class Bias(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    type = models.CharField(max_length=45, blank=False, null=False)


class Suggestion(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    corrected_description = models.TextField(blank=False, null=False)
    highlight_words = models.TextField(blank=False, null=False)


class Offer(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=45, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    salary = models.FloatField(blank=False, null=False)
    sectors = models.CharField(blank=False, null=False, max_length=45)
    key_words = models.CharField(blank=False, null=False, max_length=45)
    study_level = models.CharField(blank=False, null=False, max_length=45)
    charge = models.CharField(blank=False, null=False, max_length=45)
    location = models.CharField(blank=False, null=False, max_length=45)
    bias = models.ForeignKey(Bias, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Report(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    critical_words = models.JSONField(blank=False, null=False)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)