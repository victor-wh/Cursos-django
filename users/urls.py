from django.conf.urls import url, include
from users.views import UserLoginAPIView

urlpatterns = [
   url(r'^login/$',UserLoginAPIView.as_view() ,name="login"),
]
