from django.db import models as m
from .models import Criterias
from .decisionScenarios import DecisionScenarios

class WeightsData(m.Model):
    weightsID = m.OneToOneField(DecisionScenarios, primary_key=True, on_delete=m.CASCADE, to_field="weightID")
    criteriaID = m.ForeignKey(Criterias, on_delete=m.CASCADE)
    size = m.IntegerField()


class DataElements(m.Model):
    weightsID = m.ForeignKey(WeightsData, on_delete=m.CASCADE)
    x = m.IntegerField()
    value = m.FloatField()
