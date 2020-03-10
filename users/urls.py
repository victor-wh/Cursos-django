from django.conf.urls import url, include
from users.views import UserLoginAPIView, UserSignUpAPIView

urlpatterns = [
   url(r'^login/$',UserLoginAPIView.as_view() ,name="login"),
   url(r'^signup/$',UserSignUpAPIView.as_view() ,name="signup"),
]
