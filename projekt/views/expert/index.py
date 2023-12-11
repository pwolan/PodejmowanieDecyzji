import uuid

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView

from projekt.forms.forms import ModelForms, SubmitScenarioForm
from projekt.models import DecisionScenarios,ModelExperts,Models
from django.contrib.auth.hashers import make_password

class ExpertPanel(ListView):
    template_name = "projekt/expert_panel.html"
    model = ModelExperts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scenarios'] = DecisionScenarios.objects.filter(modelID__modelexperts__expertID=self.request.user.pk)
        print(context['scenarios'])
        return context