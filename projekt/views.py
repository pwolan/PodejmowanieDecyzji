from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from .models.models import *
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


def main(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
