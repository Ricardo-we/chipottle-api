from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
def hello_world(request):
    return HttpResponse(request, '<h1>Hello world</h1>')

