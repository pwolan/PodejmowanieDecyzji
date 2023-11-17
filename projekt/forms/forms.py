from django import forms

from ..models.models import Models


class ModelForms(forms.ModelForm):
    class Meta:
        model = Models
        fields = ['ranking_method', 'aggregation_method', 'completness_required']