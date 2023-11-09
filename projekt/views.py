from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def main(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
