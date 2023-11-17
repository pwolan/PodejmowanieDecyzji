from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic.list import  ListView
from django.views.generic import  DetailView, CreateView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import BaseModelForm, ModelForm
from django.urls import reverse_lazy

from ..models import DecisionScenarios, Models, Criterias, ModelCriterias
from ..forms.forms import ModelForms, CriteriasForms

class ScenarioView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "projekt/scenario.html"
    permission_required = "projekt.view_decisionscenarios"
    context_object_name = "scenarios"
    def get_queryset(self):
        queryset = DecisionScenarios.objects.filter(userID=self.request.user.pk)
        return queryset

# TODO dobrze by było dodać name do tabeli DecisionScenarios żeby łatwiej się było odnaleźć userowi

class CreateScenarioView(LoginRequiredMixin, CreateView):
    model = Models
    form_class = ModelForms
    template_name = 'projekt/scenario_create.html'
    scenarioID = None
    def form_valid(self, form):
        m = form.save()
        scenario = DecisionScenarios.objects.create(userID=self.request.user, modelID=m)
        self.scenarioID = scenario.pk
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('scenario-detail', kwargs={'pk': self.scenarioID})


# @register.inclusion_tag('projekt/criterium.html')
# def criterium_tag(criterium):
#     # TODO
#     subcriterias = criterium.children.all()
#     return {'children': children}

class CreateCriteriaView(LoginRequiredMixin, CreateView):
    model = Criterias
    form_class = CriteriasForms
    template_name = 'projekt/scenario_modify_criterias.html'
    def form_valid(self, form):
        criteria = form.save()
        model = Models.objects.get(pk=self.kwargs['pk'])
        model_criterias = ModelCriterias.objects.create(modelID=model, criteriaID=criteria)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('modify-criteria', kwargs={'pk': self.kwargs['pk']})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = Models.objects.get(pk=self.kwargs['pk'])
        my_objects = ModelCriterias.objects.filter(modelID=model)
        lista = dict()
        for obj in my_objects:
            key = obj.criteriaID.parent_criterion
            if key not in lista:
                lista[obj.criteriaID.parent_criterion] = []
            lista[obj.criteriaID.parent_criterion].append(obj.criteriaID.id)
        context['criterias'] = my_objects
        context['lista'] = lista
        return context

class ScenarioDetailView(LoginRequiredMixin, DetailView):
    model = DecisionScenarios
    template_name = 'projekt/scenario_detail.html'

# class CriteriaForm(ModelForm):
#     class Meta:
#         model = 

# class ModifyCriteriasView(LoginRequiredMixin, View):


# [root]

#     [critera1]
#         [subcriteria1]
#     [criteria2]


#     [criteria 3]

    # [add new criteria]
