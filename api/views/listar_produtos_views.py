from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse


def buscar_produtos(request):
    if request.method == 'POST':
        return JsonResponse({
            "success": True
        })
        
    return JsonResponse({
            "success": False
        }), render(request, 'index.html')