from django.contrib.auth.views import LoginView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from projekt.models import Experts

from projekt.forms.forms import RegisterUserForm


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))




class MyRegisterView(FormView):
    redirect_authenticated_user = True
    template_name = "registration/register.html"
    form_class = RegisterUserForm
    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print("FORM VALID")
        user = form.save()
        print(user)
        expert = Experts(user=user, name=user.username, address="address")
        expert.save()
        return super().form_valid(form)