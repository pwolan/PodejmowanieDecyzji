from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from .models.models import *
from .models.weights import *
from .models.matrices import *
from .models.decisionScenarios import *
from .serializers import*
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django import forms
from django.views.generic.edit import  FormView
# Create your views here.
@login_required
def index(request):
    return render(request, "projekt/index.html")
class ScenarioForm(forms.Form):
    modelID = forms.IntegerField()
    dataID = forms.IntegerField()
    weightID = forms.IntegerField()


class ScenarioFormView(FormView):
    template_name = "projekt/scenario_form.html"
    form_class = ScenarioForm
    success_url = "/"






class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


# class DecisionScenario(View):
#     def post(self, request):
#         print(request.data)
#         return Response({"Hello": "Hello"})


# class GetModel(viewsets.ModelViewSet):
#     queryset = Models.objects.all()
#     serializer_class = ModelsSerializer
#     def list(self, request, *args, **kwargs):
#         data = list(Models.objects.all().values())
#         return Response(data)
#
# class GetExperts(viewsets.ModelViewSet):
#     queryset = Experts.objects.all()
#     serializer_class = ExpertSerializer
#
# class GetModelExpert(viewsets.ModelViewSet):
#     queryset = ModelExperts.objects.all()
#     serializer_class = ModelExpertSerializer
#
# class GetCriterias(viewsets.ModelViewSet):
#     queryset = Criterias.objects.all()
#     serializer_class = CriteriasSerializer
#
# class GetModelCriterias(viewsets.ModelViewSet):
#     queryset = ModelCriterias.objects.all()
#     serializer_class = ModelCriteriasSerializer
#
# class GetWeightsCriterias(viewsets.ModelViewSet):
#     queryset = WeightsCriterias.objects.all()
#     serializer_class = WeightsCriteriasSerializer
#
# class GetDataElements(viewsets.ModelViewSet):
#     queryset = DataElements.objects.all()
#     serializer_class = DataElementsSerializer
#
# class GetMatrices(viewsets.ModelViewSet):
#     queryset = Matrices.objects.all()
#     serializer_class = MatricesSerializer
#
# class GetMatriceElements(viewsets.ModelViewSet):
#     queryset = MatriceElements.objects.all()
#     serializer_class = MatriceElementsSerializer
#
# class GetDataMatrices(viewsets.ModelViewSet):
#     queryset = DataMatrices.objects.all()
#     serializer_class = DataMatricesSerializer
#
# class GetDecisionScenarios(viewsets.ModelViewSet):
#     queryset = DecisionScenarios.objects.all()
#     serializer_class = DecisionScenariosSerializer


