from django.conf.urls import url, include
from users.views import UserLoginAPIView, UserSignUpAPIView, AccountVerificationAPIView

urlpatterns = [
   url(r'^login/$',UserLoginAPIView.as_view() ,name="login"),
   url(r'^signup/$',UserSignUpAPIView.as_view() ,name="signup"),
   url(r'^verify/$',AccountVerificationAPIView.as_view(), name="verify"),
]
