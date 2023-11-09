from django.db import models as m
from .models import Models
from .weights import Weights
from .matrices import Data


class DecisionScenarios(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    dataID = m.ForeignKey(Data, on_delete=m.CASCADE)
    weightID = m.ForeignKey(Weights, on_delete=m.CASCADE)