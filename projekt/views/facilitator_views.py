from django import forms
from django.views.generic.list import  ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from ..models import DecisionScenarios

# class ScenarioForm(forms.Form):
#     modelID = forms.IntegerField()
#     dataID = forms.IntegerField()
#     weightID = forms.IntegerField()
#


class ScenarioView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    template_name = "projekt/scenario.html"
    model = DecisionScenarios
    permission_required = "projekt.view_decisionscenarios"

