from django import forms
from django.db import transaction
from django.forms.utils import ErrorList

from ..models import DataMatrices, Matrices, MatriceElements
from ..models.models import Models, Criterias, Alternatives, ModelScales, Scales, Experts
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
        
class CriteriasDeleteForm(forms.ModelForm):
    class Meta:
        model = Criterias
        fields = ['name']
    def __init__(self, **kwargs):
        q = kwargs.pop("form_q")
        super(CriteriasDeleteForm, self).__init__(**kwargs)
        self.fields['name'] = forms.ModelChoiceField(queryset=q)


class AlternativesForm(forms.ModelForm):
    class Meta:
        model = Alternatives
        fields = ["name", "description"]

class SubmitScenarioForm(forms.Form):
    password = forms.CharField(label="Password (If not set, password not used)", required=False)
class EndScenarioForm(forms.Form):
    password = forms.CharField(label="Password (If not set, password not used)", required=False)

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

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
        self.criterias = kwargs.pop("criterias")
        self.user = kwargs.pop("user")
        self.parent = kwargs.pop("parent")
        self.model = kwargs.pop("model")
        self.size = len(self.criterias)
        scales = Scales.objects.filter(modelscales__modelID=self.model)
        choices = [(s.value, s.description) for s in scales]
        expert = Experts.objects.get(user_id=self.user)
        # adding matrices
        matrix, _ = Matrices.objects.update_or_create(criteriaID=self.parent, expertID=expert, size=self.size)
        decisionscenario = DecisionScenarios.objects.get(modelID=self.model)
        dataMatrix, _ = DataMatrices.objects.update_or_create(dataID=decisionscenario, matrixID=matrix)

        super().__init__(*args, **kwargs)
        for x,cr1 in enumerate(self.criterias):
            for y,cr2 in enumerate(self.criterias):
                if cr1['id'] < cr2['id']:
                    el_exists = MatriceElements.objects.filter(matrixID=matrix, x=x, y=y).exists()
                    initial = None
                    if el_exists:
                        initial = MatriceElements.objects.get(matrixID=matrix, x=x, y=y).value
                        widget = forms.Select(attrs={'class': 'exists'})
                    else:
                        initial = choices[len(choices)//2]
                        widget = forms.Select()
                    self.fields[self._get_field_name(cr1,cr2)] = forms.ChoiceField(label="", choices=choices, initial=initial, widget=widget)

    def save(self, user, parent):
        # print("SAVING OR UPDATING")

        with transaction.atomic(): # tranzakcja, żeby wszystko na raz się zapisało albo nic
            expert = Experts.objects.get(user_id=user)
            # adding matrices
            matrix,_ = Matrices.objects.update_or_create(criteriaID=parent, expertID=expert,size=self.size)
            decisionscenario = DecisionScenarios.objects.get(modelID=self.model)
            dataMatrix,_ = DataMatrices.objects.update_or_create(dataID=decisionscenario, matrixID=matrix)
            for x,cr1 in enumerate(self.criterias):
                for y,cr2 in enumerate(self.criterias):
                    if cr1['id'] < cr2['id']:
                        MatriceElements.objects.update_or_create(matrixID=matrix, x=x, y=y, defaults={"value":self._get_field_value(cr1,cr2)})
                    elif cr1['id'] == cr2['id']:
                        MatriceElements.objects.update_or_create(matrixID=matrix, x=x, y=y, value=1)
                    else:
                        MatriceElements.objects.update_or_create(matrixID=matrix, x=x, y=y, defaults={"value":self._get_field_value(cr2,cr1)})
    def _get_field_name(self, id1,id2):
        return "_" + str(id1['id']) + "-" + str(id2['id'])

    def _get_field_value(self, id1,id2):
        return self.cleaned_data.get(self._get_field_name(id1,id2))