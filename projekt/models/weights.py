from django.db import models
from .models import Criterias


class Weights(models.Model):
    pass


class WeightData(models.Model):
    size = models.IntegerField()


class DataElement(models.Model):
    weightDataID = models.ForeignKey(WeightData, on_delete=models.CASCADE)
    expertlDorXValue = models.IntegerField()
    value = models.FloatField()


class WeightsCriterias(models.Model):
    weightID = models.ForeignKey(Weights, on_delete=models.CASCADE)
    criteriaID = models.ForeignKey(Criterias, on_delete=models.CASCADE)
    weightDataID = models.ForeignKey(WeightData, on_delete=models.CASCADE)
