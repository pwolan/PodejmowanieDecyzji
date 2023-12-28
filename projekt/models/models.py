from django.db import models as m
from django.contrib.auth.models import User


class Models(m.Model):
    RANKING_METHODS = [
        ('GMM', 'Geometric Mean Method'),
    ]
    AGGREGATION_METHODS = [
        ('AIP', 'Aggregation of individual priorities'),
    ]
    ranking_method = m.CharField(max_length=4, choices=RANKING_METHODS, default='GMM')
    aggregation_method = m.CharField(max_length=4, choices=AGGREGATION_METHODS, default='AIP')
    completeness_required = m.BooleanField(default=True)
    criteriasDone = m.BooleanField(default=False)
    expertsDone = m.BooleanField(default=False)
    scaleDone = m.BooleanField(default=False)
    alternativesDone = m.BooleanField(default=False)



class Alternatives(m.Model):
    name = m.CharField(max_length=30)
    description = m.CharField(max_length=150)


class ModelAlternatives(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    alternativeID = m.ForeignKey(Alternatives, on_delete=m.CASCADE)


class Scales(m.Model):
    value = m.FloatField(unique=True)
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
    done = m.BooleanField(default=False)
    
    class Meta:
        unique_together = ['modelID', 'expertID']


class Criterias(m.Model):
    parent_criterion = m.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=m.CASCADE)
    name = m.CharField(max_length=50)
    description = m.CharField(max_length=150)


class ModelCriterias(m.Model):
    modelID = m.ForeignKey(Models, on_delete=m.CASCADE)
    criteriaID = m.ForeignKey(Criterias, on_delete=m.CASCADE)


