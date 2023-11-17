from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.list import  ListView
from django.views.generic import  DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import BaseModelForm, ModelForm


from ..models import DecisionScenarios, Models
from ..forms.forms import ModelForms
from django.contrib.auth.decorators import login_required

# class ScenarioForm(forms.Form):
#     modelID = forms.IntegerField()
#     dataID = forms.IntegerField()
#     weightID = forms.IntegerField()
#


class ScenarioView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "projekt/scenario.html"
    permission_required = "projekt.view_decisionscenarios"
    context_object_name = "scenarios"
    def get_queryset(self):
        queryset = DecisionScenarios.objects.filter(userID=self.request.user.pk)
        return queryset

# TODO dobrze by było dodać name do tabeli DecisionScenarios żeby łatwiej się było odnaleźć userowi
# @login_required
# def add_scenario(request):
#     scenario = DecisionScenarios.objects.create(userID=request.user)
#     return redirect('scenario-detail', scenario.pk)
class CreateScenarioView(LoginRequiredMixin, CreateView):
    model = Models
    form_class = ModelForms
    template_name = 'projekt/scenario_create.html'
    def form_valid(self, form):
        m = form.save()
        DecisionScenarios.objects.create(userID=self.request.user.pk, ModelID=m.pk)
        # tutaj można wykonać dodatkowe akcje po poprawnym wysłaniu formularza
        return super().form_valid(form)

class ScenarioDetailView(LoginRequiredMixin, DetailView):
    model = DecisionScenarios
    template_name = 'projekt/scenario_detail.html'

# class CriteriaForm(ModelForm):
#     class Meta:
#         model = 

# class ModifyCriteriasView(LoginRequiredMixin, View):

