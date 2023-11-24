from django.db import models as m
from .models import Models
from django.contrib.auth.models import User


class DecisionScenarios(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE, null=True, blank=True)
    dataID = m.IntegerField(unique=True)
    weightID = m.IntegerField(unique=True)
    userID = m.ForeignKey(User, on_delete=m.CASCADE)
