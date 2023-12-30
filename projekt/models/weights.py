from django.db import models as m
from .models import Criterias
from .decisionScenarios import DecisionScenarios

class DataWeights(m.Model):
    criteriaID = m.ForeignKey(Criterias, on_delete=m.CASCADE)
    size = m.IntegerField()

class DataElements(m.Model):
    dataWeightsID = m.ForeignKey(DataWeights, on_delete=m.CASCADE, default=None)
    x = m.IntegerField()
    value = m.FloatField()

class ScenarioWeights(m.Model):
    weightsID = m.ForeignKey(DecisionScenarios, on_delete=m.CASCADE, to_field="weightID")
    dataWeights = m.ForeignKey(DataWeights, on_delete=m.CASCADE)