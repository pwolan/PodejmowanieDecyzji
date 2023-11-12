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
from rest_framework.response import Response
# Create your views here.
class GetModel(viewsets.ModelViewSet):
    queryset = Models.objects.all()
    serializer_class = ModelsSerializer
    def list(self, request, *args, **kwargs):
        data = list(Models.objects.all().values())
        return Response(data)

class GetExperts(viewsets.ModelViewSet):
    queryset = Experts.objects.all()
    serializer_class = ExpertSerializer

class GetModelExpert(viewsets.ModelViewSet):
    queryset = ModelExperts.objects.all()
    serializer_class = ModelExpertSerializer

class GetCriterias(viewsets.ModelViewSet):
    queryset = Criterias.objects.all()
    serializer_class = CriteriasSerializer

class GetModelCriterias(viewsets.ModelViewSet):
    queryset = ModelCriterias.objects.all()
    serializer_class = ModelCriteriasSerializer

class GetWeightsCriterias(viewsets.ModelViewSet):
    queryset = WeightsCriterias.objects.all()
    serializer_class = WeightsCriteriasSerializer

class GetDataElements(viewsets.ModelViewSet):
    queryset = DataElements.objects.all()
    serializer_class = DataElementsSerializer

class GetMatrices(viewsets.ModelViewSet):
    queryset = Matrices.objects.all()
    serializer_class = MatricesSerializer

class GetMatriceElements(viewsets.ModelViewSet):
    queryset = MatriceElements.objects.all()
    serializer_class = MatriceElementsSerializer

class GetDataMatrices(viewsets.ModelViewSet):
    queryset = DataMatrices.objects.all()
    serializer_class = DataMatricesSerializer

class GetDecisionScenarios(viewsets.ModelViewSet):
    queryset = DecisionScenarios.objects.all()
    serializer_class = DecisionScenariosSerializer

def main(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
