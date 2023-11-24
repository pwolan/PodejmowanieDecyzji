from django import forms

from ..models.models import Models, Criterias
from ..models.models import Models, ModelCriterias

class ModelForms(forms.ModelForm):
    class Meta:
        model = Models
        fields = ['ranking_method', 'aggregation_method', 'completeness_required']

class CriteriasForms(forms.ModelForm):
    class Meta:
        model = Criterias
        fields = ['parent_criterion', 'name', 'description']
    def __init__(self, **kwargs):
        q = kwargs.pop("form_q")
        super(CriteriasForms, self).__init__(**kwargs)
        self.fields['parent_criterion'] = forms.ModelChoiceField(queryset=q)
