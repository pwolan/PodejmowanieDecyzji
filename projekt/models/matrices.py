from django.db import models as m
from .models import Experts, Criterias


class Matrices(m.Model):
    expertID = m.ForeignKey(Experts, on_delete=m.CASCADE)
    criteriaID = m.ForeignKey(Criterias, on_delete=m.CASCADE)
    rowSize = m.IntegerField()
    columnSize = m.IntegerField()


class MatriceElements(m.Model):
    matrixID = m.ForeignKey(Matrices, on_delete=m.CASCADE)
    x = m.IntegerField()
    y = m.IntegerField()
    value = m.FloatField()


class Data(m.Model):
    pass


class DataMatrices(m.Model):
    dataID = m.ForeignKey(Data, on_delete=m.CASCADE)
    MatrixID = m.ForeignKey(Matrices, on_delete=m.CASCADE)


