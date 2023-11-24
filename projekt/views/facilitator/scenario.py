from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from projekt.forms.forms import ModelForms
from projekt.models import DecisionScenarios, Models, Criterias, ModelCriterias


class ScenarioView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "projekt/scenario.html"
    permission_required = "projekt.view_decisionscenarios"
    context_object_name = "scenarios"
    def get_queryset(self):
        queryset = DecisionScenarios.objects.filter(userID=self.request.user.pk)
        return queryset


class CreateScenarioView(LoginRequiredMixin, CreateView):
    model = Models
    form_class = ModelForms
    template_name = 'projekt/scenario_create.html'
    scenarioID = None
    def form_valid(self, form):
        m = form.save()
        scenario = DecisionScenarios.objects.create(userID=self.request.user, modelID=m)
        self.scenarioID = scenario.pk
        rootCriterion = Criterias(name="Root", description="Root Criterion")
        rootCriterion.save()
        modelCriteriasRoot = ModelCriterias(criteriaID=rootCriterion, modelID=m)
        modelCriteriasRoot.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('scenario-detail', kwargs={'pk': self.scenarioID})


class ScenarioDetailView(LoginRequiredMixin, DetailView):
    model = DecisionScenarios
    template_name = 'projekt/scenario_detail.html'
