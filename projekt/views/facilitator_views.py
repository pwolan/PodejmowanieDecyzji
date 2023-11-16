from django.shortcuts import redirect
from django.views.generic.list import  ListView
from django.views.generic import  DetailView, CreateView
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

# TODO dobrze by było dodać name do tabeli DecisionScenarios żeby łatwiej się było odnaleźć userowi
def add_scenario(request):
    scenario = DecisionScenarios.objects.create()
    return redirect('scenario-detail', scenario.pk)
# TODO trzeba dodać userID do decisionScenarios żeby było wiadomo kto to stworzył
class ScenarioDetailView(DetailView):
    # model = DecisionScenarios
    template_name = 'projekt/scenario_detail.html'
    # queryset = DecisionScenarios.objects.filter()


