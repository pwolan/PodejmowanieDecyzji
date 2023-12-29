from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from projekt.forms.forms import AlternativeDecisionForm
from projekt.models import DecisionScenarios, Models, Alternatives, Criterias, Matrices, DataMatrices
from projekt.methods_matrices import make_decision_tree
import pdb




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
        matrices = DataMatrices.objects.filter(dataID=scenario)
        completed = len(matrices)
        context['progress'] = f"Uzupełniono {completed}/{len(tree)}"

        return context


class QuestionareCriteriumView(LoginRequiredMixin,FormView):
    template_name = 'projekt/questionare_criterium.html'
    form_class = AlternativeDecisionForm
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.scenario = DecisionScenarios.objects.get(url=self.kwargs['url'])
        self.model = Models.objects.get(decisionscenarios=self.scenario)
        self.criterium = Criterias.objects.get(pk=self.kwargs['pk'])
        self.children = Criterias.objects.filter(parent_criterion=self.criterium)

    def get_success_url(self):
        return reverse('questionare-criterium', kwargs={'url': self.kwargs['url'], 'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.save(self.request.user, self.criterium)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if len(self.children) == 0:
            alternatives = Alternatives.objects.filter(
                modelalternatives__modelID__decisionscenarios=self.scenario)
            kwargs.update({
                "model": self.model,
                "criterias": alternatives.values(),
                "user": self.request.user,
                "parent": self.criterium
            })
            return kwargs
        else:
            kwargs.update({
                "model": self.model,
                "criterias": self.children.values(),
                "user": self.request.user,
                "parent": self.criterium
            })
            return kwargs



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['criterium'] = self.criterium
       
        if len(self.children) == 0:
            context['alternatives'] = Alternatives.objects.filter(modelalternatives__modelID__decisionscenarios=self.scenario)
        else:
            context['criterions'] = self.children

        context['url'] = self.kwargs['url']
        return context
