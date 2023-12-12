from django.db import models as m
from django.contrib.auth.models import User


class Models(m.Model):
    ranking_method = m.CharField(max_length=4)
    aggregation_method = m.CharField(max_length=4)
    completeness_required = m.BooleanField()
    criteriasDone = m.BooleanField(default=False)
    expertsDone = m.BooleanField(default=False)
    scaleDone = m.BooleanField(default=False)
    alternativesDone = m.BooleanField(default=False)


class Alternatives(m.Model):
    name = m.CharField(max_length=20)
    description = m.CharField(max_length=100)


class ModelAlternatives(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    alternativeID = m.ForeignKey(Alternatives, on_delete=m.CASCADE)


class Scales(m.Model):
    value = m.FloatField()
    description = m.CharField(max_length=100)


class ModelScales(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    scaleID = m.ForeignKey(Scales, on_delete=m.CASCADE)


# TODO to w sumie może być po prostu user, on też ma name i address email
class Experts(m.Model):
    user = m.OneToOneField(
        User,
        on_delete=m.DO_NOTHING,
        primary_key=False,
        default=0
    )
    name = m.CharField(max_length=50)
    address = m.CharField(max_length=50)


class ModelExperts(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    expertID = m.ForeignKey(Experts, on_delete=m.CASCADE)
    
    class Meta:
        unique_together = ['modelID', 'expertID']


class Criterias(m.Model):
    parent_criterion = m.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=m.CASCADE)
    name = m.CharField(max_length=50)
    description = m.CharField(max_length=100)


class ModelCriterias(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    criteriaID = m.ForeignKey(Criterias, on_delete=m.CASCADE)


