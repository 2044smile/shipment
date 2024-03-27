from django.urls import path
from accounts.views import KakaoLoginView


urlpatterns = [
    path('kakao/', KakaoLoginView.as_view(), name="kakao_login"),
]
