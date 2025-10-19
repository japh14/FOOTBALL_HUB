# from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View

class StatusView(View):
    def get(self, request):
        return JsonResponse({'status': 'ok', 'message': 'Connected to Django API!'})


def home(request):
    return HttpResponse("Welcome to the Home Page - Football Hub API (nginx reload test)")