from django.db import models as m
from .models import Models
from .weights import Weights
from .matrices import Data
from django.contrib.auth.models import User


class DecisionScenarios(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE, null=True, blank=True)
    dataID = m.ForeignKey(Data, on_delete=m.CASCADE, null=True, blank=True)
    weightID = m.ForeignKey(Weights, on_delete=m.CASCADE, null=True, blank=True)
    userID = m.ForeignKey(User, on_delete=m.CASCADE)
