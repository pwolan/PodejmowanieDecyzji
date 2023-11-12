from django.db import models
from .models import Criterias


class Weights(models.Model):
    pass

class WeightsCriterias(models.Model):
    weightID = models.ForeignKey(Weights, on_delete=models.CASCADE)
    criteriaID = models.ForeignKey(Criterias, on_delete=models.CASCADE)
    weightDataID = models.IntegerField(unique=True)
    Size = models.IntegerField(default=0)


class DataElements(models.Model):
    weightDataID = models.ForeignKey(WeightsCriterias, on_delete=models.CASCADE, to_field="weightDataID")
    expertlDorXValue = models.IntegerField()
    value = models.FloatField()
