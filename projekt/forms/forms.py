from django import forms
from django.forms.utils import ErrorList

from ..models.models import Models, Criterias, Alternatives
from ..models.models import Models, ModelCriterias
from ..models.decisionScenarios import DecisionScenarios
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


class AlternativesForm(forms.ModelForm):
    class Meta:
        model = Alternatives
        fields = ["name", "description"]

class SubmitScenarioForm(forms.Form):
    password = forms.CharField(label="Password (If not set, password not used)", required=False)


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

def validate_url(url):
    if not DecisionScenarios.objects.filter(url=url).exists():
        raise ValidationError(
            _("%(url)s is not valid url"),
            params={"url": url},
        )

class JoinScenarioForm(forms.Form):
    url = forms.CharField(label="Tutaj wpisz kod od facylitatora", required=True, validators=[validate_url])

class AlternativeDecisionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        criterias = kwargs.pop("criterias")
        prefix = kwargs.pop("prefix")
        super().__init__(*args, **kwargs)
        for criterium in criterias:
            print(criterium)
            self.fields[prefix+"_"+str(criterium['id'])] = forms.DecimalField(label="")


    def save(self):
        pass