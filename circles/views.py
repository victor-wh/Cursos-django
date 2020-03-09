# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Django REST Framework
from rest_framework.decorators import api_view
#models
from circles.models import Circle

# Create your views here.
def list_circles(request):
    circles = Circle.objects.all()
    public = circles.filter(is_public=True)
    data = []
    for circle in public:
        data.append({
            'name': circle.name,
            'slug_name': circle.slug_name,
            'rides_taken': circle.rides_taken,
            'rides_offered': circle.rides_offered,
            'members_limit': circle.members_limit,
        })
    return JsonResponse(data, safe=False)