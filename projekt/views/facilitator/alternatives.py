from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from projekt.models import Alternatives, DecisionScenarios, ModelAlternatives
from projekt.forms.forms import AlternativesForm


class CreateAlternativesView(LoginRequiredMixin, CreateView):
    model = Alternatives
    form_class = AlternativesForm
    template_name = 'scenario/scenario_modify_alternatives.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        model = scenario.modelID
        context['alternatives'] = Alternatives.objects.filter(modelalternatives__modelID=model)
        context['scenario'] = scenario
        print(context['alternatives'])
        return context
    def get_success_url(self):
        return reverse_lazy('modify-alternatives', kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        alternative = form.save()
        scenario = DecisionScenarios.objects.get(pk=self.kwargs['pk'])
        model = scenario.modelID
        model_alternatives = ModelAlternatives.objects.create(modelID=model, alternativeID=alternative)
        return super().form_valid(form)

class DeleteAlternativesView(LoginRequiredMixin, DeleteView):
    model = Alternatives

    template_name = 'scenario/scenario_delete_alternatives.html'

    def form_valid(self, form):
        model = Alternatives.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('modify-alternatives', kwargs={'pk': self.kwargs['scenarioId']})
