import uuid

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView

from projekt.forms.forms import ModelForms, SubmitScenarioForm
from projekt.models import DecisionScenarios, Models, Criterias, ModelCriterias
from django.contrib.auth.hashers import make_password

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
        return reverse_lazy('modify-criteria', kwargs={'pk': self.kwargs['pk']})


class ScenarioDetailView(LoginRequiredMixin, DetailView):
    model = DecisionScenarios
    template_name = 'projekt/scenario_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(pk=self.kwargs.get('pk'))
        if scenario.submited:
            # context['link'] = reverse_lazy('questionare', kwargs={'url':scenario.url})
            context['link'] =  scenario.url
        return context


class ScenarioSubmitView(FormView):
    template_name = "projekt/scenario_submit.html"
    form_class = SubmitScenarioForm
    def get_success_url(self):
        return reverse_lazy('scenario-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        scenario.submited = True
        scenario.url = str(uuid.uuid4())[:12]
        scenario.password = make_password(form.cleaned_data.get('password'))
        scenario.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(pk=self.kwargs.get('pk'))
        context['scenario'] = scenario
        return context
