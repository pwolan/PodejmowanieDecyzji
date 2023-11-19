from django.db import models as m
from .models import Experts, Criterias
from .decisionScenarios import DecisionScenarios


class Matrices(m.Model):
    expertID = m.ForeignKey(Experts, on_delete=m.CASCADE, null=True)
    criteriaID = m.ForeignKey(Criterias, on_delete=m.CASCADE, null=True)
    rowSize = m.IntegerField()
    columnSize = m.IntegerField()


class MatriceElements(m.Model):
    matrixID = m.ForeignKey(Matrices, on_delete=m.CASCADE)
    x = m.IntegerField()
    y = m.IntegerField()
    value = m.FloatField()


class DataMatrices(m.Model):
    dataID = m.ForeignKey(DecisionScenarios, on_delete=m.CASCADE, to_field="dataID")
    matrixID = m.ForeignKey(Matrices, on_delete=m.CASCADE)


