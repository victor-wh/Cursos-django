from django.conf.urls import url, include
from circles.views import list_circles, probar, create_circle

urlpatterns = [
   url(r'^circles/$',list_circles,name="circulos"),
   url(r'^circles/create/$',create_circle, name="crear_circulos"),
   url(r'^probar/$',probar),
]
