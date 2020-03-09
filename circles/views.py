# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
#Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import requests
#models
from circles.models import Circle
# Serializer
from circles.serializers import CircleSerializer, CreateCircleSerializer

# Create your views here.
@api_view(['GET'])
def list_circles(request):
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles,many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def create_circle(request):
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)
 # para probar el post
def probar(request):
    headers = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {
        'name': 'Manzana',
        'slug_name':'manzana',
    }
    r = requests.post('http://127.0.0.1:8000/circles/create/', headers=headers, data=data)

    return HttpResponse(r.text)