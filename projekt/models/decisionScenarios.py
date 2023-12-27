from django.db import models as m
from .models import Models
from django.contrib.auth.models import User


class DecisionScenarios(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE, null=True, blank=True)
    dataID = m.IntegerField(unique=True, null=True, blank=True)
    weightID = m.IntegerField(unique=True, null=True, blank=True)
    userID = m.ForeignKey(User, on_delete=m.CASCADE)
    submited = m.BooleanField(default=False)
    completed = m.BooleanField(default=False)
    url = m.CharField(max_length=100, null=True, blank=True)
    password = m.CharField(max_length=128, null=True, blank=True)