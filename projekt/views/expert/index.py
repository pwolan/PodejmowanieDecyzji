import uuid

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView

from projekt.forms.forms import ModelForms, SubmitScenarioForm, JoinScenarioForm
from projekt.models import DecisionScenarios,ModelExperts, Models, Experts
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
        context['scenarios'] = DecisionScenarios.objects.filter(modelID__modelexperts__expertID=self.request.user.pk)
        print(context['scenarios'])
        return context
    
    def form_valid(self, form): 
        url = form.cleaned_data.get('url')
        expertID = Experts.objects.get(user_id=self.request.user.pk)
        modelID = None
        modelID = Models.objects.get(id=DecisionScenarios.objects.get(url=url).modelID_id)  
        if not ModelExperts.objects.filter(expertID=expertID, modelID=modelID).exists():
            connection = ModelExperts.objects.create(modelID=modelID, expertID=expertID)
            connection.save()
        else:
            form.add_error('url', 
                ValidationError(
                    _("%(url)s jesteś już w tym urlu"),
                    params={"url": url},
                )
            )
            return super().form_invalid(form)

        return super().form_valid(form)
