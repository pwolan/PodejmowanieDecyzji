import uuid

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView,TemplateView

from projekt.forms.forms import ModelForms, SubmitScenarioForm, JoinScenarioForm, AlternativeDecisionForm
from projekt.models import DecisionScenarios, ModelExperts, Models, Experts, Alternatives,Criterias
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ExpertPanel(FormView):
    template_name = "projekt/expert_panel.html"
    model = ModelExperts
    form_class = JoinScenarioForm

    def get_success_url(self):
        return reverse_lazy('expert-panel')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expertID = Experts.objects.get(user_id=self.request.user.pk)
        context['scenarios'] = DecisionScenarios.objects.filter(modelID__modelexperts__expertID=expertID)
        return context
    
    def form_valid(self, form): 
        url = form.cleaned_data.get('url')
        expertID = Experts.objects.get(user_id=self.request.user.pk)
        modelID = Models.objects.get(id=DecisionScenarios.objects.get(url=url).modelID_id)
    
        scenario = DecisionScenarios.objects.get(modelID=modelID) 
        print(scenario)
        if not ModelExperts.objects.filter(expertID=expertID, modelID=modelID).exists() and not scenario.completed:
            connection = ModelExperts.objects.create(modelID=modelID, expertID=expertID)
            connection.save()
        elif scenario.completed:
            form.add_error('url', 
                ValidationError(
                    _("%(url)s ankieta się już zakończyła"),
                    params={"url": url},
                )
            )
            return super().form_invalid(form)
        else:
            form.add_error('url', 
                ValidationError(
                    _("%(url)s jesteś już w tym urlu"),
                    params={"url": url},
                )
            )
            return super().form_invalid(form)

        return super().form_valid(form)


class QuestionareView(TemplateView):
    template_name = 'projekt/questionare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(url=self.kwargs['url'])
        # print(scenario)
        alternatives = Alternatives.objects.filter(modelalternatives__modelID__decisionscenarios=scenario)
        # print(alternatives)
        context['alternatives'] = alternatives
        context['url'] = self.kwargs['url']
        return context





class AlternativesDecisionView(TemplateView):
    template_name = 'projekt/alternatives_decision.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alt1 = Alternatives.objects.get(pk=self.kwargs['alt1'])
        alt2 = Alternatives.objects.get(pk=self.kwargs['alt2'])
        context['alt1'] = alt1
        context['alt2'] = alt2
        # get criterias
        model = Models.objects.get(decisionscenarios__url=self.kwargs['url'])
        criterias = Criterias.objects.filter(modelcriterias__modelID=model)
        context['criterias'] = criterias

        # make form
        context['form'] = AlternativeDecisionForm(model=model,prefix="alt", criterias=criterias.values())
        # context['form2'] = AlternativeDecisionForm(prefix="alt2", criterias=criterias.values())
        context['len'] = len(criterias.values())+1
        return context