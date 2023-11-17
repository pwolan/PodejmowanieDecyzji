from django import forms

from ..models.models import Models, Criterias


class ModelForms(forms.ModelForm):
    class Meta:
        model = Models
        fields = ['ranking_method', 'aggregation_method', 'completness_required']

class CriteriasForms(forms.ModelForm):
    class Meta:
        model = Criterias
        fields = ['parent_criterion', 'name', 'description']