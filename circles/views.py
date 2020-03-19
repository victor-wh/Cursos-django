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
        'email':'develop1@gmail.com',
        'first_name': 'Victor',
        'last_name': 'Albornoz',
        'username': 'develop1',
        'password':'temporal',
        'password_confirmation': 'temporal',
        'phone_number':'9983950079',

    }
    data_login = {
        'email':'develop1@gmail.com',
        'password':'temporal',
    }
    data_token = {
        'token':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiZW1haWxfY29uZmlybWF0aW9uIiwidXNlciI6ImRldmVsb3AxIiwiZXhwIjoxNTg0OTAzOTgyfQ.jFizGpCy4hIYkMMF6nQG8E_yQgjMfaaC06Cu8Tj86Gg'
    }
    r = requests.post('http://127.0.0.1:8000/login/', headers=headers, data=data_login)

    return HttpResponse(r.text)