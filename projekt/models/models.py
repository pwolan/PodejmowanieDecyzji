from django.db import models


class Models(models.Model):
    ranking_method = models.CharField(max_length=4)
    aggregation_method = models.CharField(max_length=4)
    completness_required = models.BooleanField()

# TODO to w sumie może być po prostu user, on też ma name i address email
class Experts(models.Model):
    name = models.IntegerField()
    address = models.CharField(max_length=100)


class ModelExperts(models.Model):
    modelID = models.ForeignKey(Models, on_delete=models.CASCADE)
    expertID = models.ForeignKey(Experts, on_delete=models.CASCADE)


class Criterias(models.Model):
    parent_criterion = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)


class ModelCriterias(models.Model):
    modelID = models.ForeignKey(Models, on_delete=models.CASCADE)
    criteriaID = models.ForeignKey(Criterias, on_delete=models.CASCADE)


