from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView

from projekt.forms.forms import CriteriasForms, CriteriasDeleteForm
from projekt.models import Criterias, DecisionScenarios, ModelCriterias, Scales


class CreateCriteriaView(LoginRequiredMixin, CreateView):
    model = Criterias
    form_class = CriteriasForms
    template_name = 'scenario/scenario_modify_criterias.html'



    def form_valid(self, form):
        criteria = form.save()
        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        model = scenario.modelID
        model_criterias = ModelCriterias.objects.create(modelID=model, criteriaID=criteria)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('modify-criteria', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CreateCriteriaView, self).get_form_kwargs(*args,**kwargs)
        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        model = scenario.modelID
        form_kwargs['form_q'] = Criterias.objects.filter(modelcriterias__modelID=model)
        return form_kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        model = scenario.modelID

        my_objects = ModelCriterias.objects.filter(modelID=model.pk)
        rootCriterion = my_objects.filter(criteriaID__parent_criterion__isnull=True).first()
        context['criterias'] = rootCriterion.criteriaID
        context['scenario'] = scenario
        return context

class DeleteCriteriaView(LoginRequiredMixin, DeleteView):
    model = Criterias

    template_name = 'scenario/scenario_delete_criteria.html'

    def form_valid(self, form):
        model = Criterias.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('modify-criteria', kwargs={'pk': self.kwargs['scenarioId']})