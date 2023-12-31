from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView

from projekt.forms.forms import JoinScenarioForm
from projekt.models import DecisionScenarios, ModelExperts, Models, Experts
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