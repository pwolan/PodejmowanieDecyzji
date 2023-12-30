import uuid
import json

from django.db.models import Max
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView

from projekt.forms.forms import ModelForms, SubmitScenarioForm, EndScenarioForm
from projekt.models import DecisionScenarios, Models, Criterias, ModelCriterias, ModelExperts, Alternatives, ModelScales, Scales
from django.contrib.auth.hashers import make_password
from projekt.methods_matrices import make_decision_tree, generate_json_file

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

class ScenarioView(LoginRequiredMixin,  ListView):
    template_name = "scenario/scenario.html"
    permission_required = "projekt.view_decisionscenarios"
    context_object_name = "scenarios"
    def get_queryset(self):
        queryset = DecisionScenarios.objects.filter(userID=self.request.user.pk)
        return queryset


class CreateScenarioView(LoginRequiredMixin, CreateView):
    model = Models
    form_class = ModelForms
    template_name = 'scenario/scenario_create.html'
    scenarioID = None
    def form_valid(self, form):
        m = form.save()
        scenario = DecisionScenarios.objects.create(userID=self.request.user, modelID=m)
        self.scenarioID = scenario.pk
        rootCriterion = Criterias(name="Root", description="Root Criterion")
        rootCriterion.save()
        modelCriteriasRoot = ModelCriterias(criteriaID=rootCriterion, modelID=m)
        modelCriteriasRoot.save()
        # Dodaj wszystko z Scales do ModelScales z modelID=m
        for skala in Scales.objects.all():
            scales = ModelScales(modelID=m, scaleID=skala)
            scales.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('scenario-detail', kwargs={'pk': self.scenarioID})


class ScenarioDetailView(LoginRequiredMixin, DetailView):
    model = DecisionScenarios
    template_name = 'scenario/scenario_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(pk=self.kwargs.get('pk'))
        model = scenario.modelID
        result = DecisionScenarios.objects.aggregate(Max('dataID'))
        if not type(result['dataID__max']) == int:
            result['dataID__max'] = 0
        if type(scenario.dataID) != int:
            scenario.dataID = result['dataID__max'] + 1
            scenario.save()
        context['completeness_required'] = model.completeness_required
        context['ranking_method'] = model.ranking_method
        context['aggregation_method'] = model.aggregation_method
        if scenario.submited:
            all_experts = len(ModelExperts.objects.filter(modelID=model))
            done_experts = len(ModelExperts.objects.filter(modelID=model).filter(done=True))
            context['frac'] = done_experts - all_experts
            context['fractional_experts'] = f'{done_experts} / {all_experts}'
            context['alternatives'] = Alternatives.objects.filter(modelalternatives__modelID=model)
            my_objects = ModelCriterias.objects.filter(modelID=model.pk)
            rootCriterion = my_objects.filter(criteriaID__parent_criterion__isnull=True).first()
            context['criterias'] = rootCriterion.criteriaID
            context['link'] =  scenario.url
        context['scenario'] = scenario
        make_decision_tree(scenario)
        return context


class ScenarioSubmitView(FormView):
    template_name = "scenario/scenario_submit.html"
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
class ScenarioEndView(FormView):
    template_name = "scenario/scenario_end.html"
    form_class = EndScenarioForm
    def get_success_url(self):
        return reverse_lazy('scenario-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        scenario.completed = True
        scenario.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(pk=self.kwargs.get('pk'))
        context['scenario'] = scenario
        return context
def generate_json(request, pk):
    scenario = get_object_or_404(DecisionScenarios, pk=pk)
    name = generate_json_file(scenario)
    with open(f'{name}', 'r') as f:
        data = json.load(f)
    return JsonResponse(data)