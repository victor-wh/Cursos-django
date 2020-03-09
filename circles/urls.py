from django.conf.urls import url, include
from circles.views import list_circles

urlpatterns = [
   url(r'^circles/',list_circles),
]
