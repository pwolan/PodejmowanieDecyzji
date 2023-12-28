from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView

from projekt.forms.forms import AlternativeDecisionForm
from projekt.models import DecisionScenarios, Models, Alternatives,Criterias
from projekt.methods_matrices import make_decision_tree




class QuestionareView(TemplateView):
    template_name = 'projekt/questionare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(url=self.kwargs['url'])
        tree = make_decision_tree(scenario)
        context['tree'] = [{
                "id": t[0], 
                "link": reverse('questionare-criterium', args=[self.kwargs['url'], t[0]])
            } for t in tree]
        context['url'] = self.kwargs['url']
        return context

class QuestionareCriteriumView(TemplateView):
    template_name = 'projekt/questionare_criterium.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        scenario = DecisionScenarios.objects.get(url=self.kwargs['url'])
        criterium = Criterias.objects.get(pk=self.kwargs['pk'])
        context['criterium'] = criterium
        childreen = Criterias.objects.filter(parent_criterion = criterium)
       
        if len(childreen) == 0:
            context['alternatives'] = Alternatives.objects.filter(modelalternatives__modelID__decisionscenarios=scenario)
        else:
            context['criterions'] = childreen
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