from django.urls import path
from accounts.views import GetKakaoInfoAPIView, SignUpAPIView


app_name = 'accounts'

urlpatterns = [
    path('kakao/', GetKakaoInfoAPIView.as_view(), name="kakao_login"),
    path('signup/', SignUpAPIView.as_view(), name="signup"),
]
