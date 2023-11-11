from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from .models.models import *
from .serializers import*
from rest_framework.response import Response
# Create your views here.
class GetMethod(viewsets.ModelViewSet):
    models_queryset = Models.objects.all()
    model_serializer = ModelsSerializer
    experts_queryset = Experts.objects.all()
    experts_serializer = ExpertSerializer
    model_expert_queryset = ModelExperts.objects.all()
    model_expert_serializer = ModelExpertSerializer


def main(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
