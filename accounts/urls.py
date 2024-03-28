from django.urls import path
from accounts.views import GetKakaoInfoAPIView, SignUpAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = 'accounts'

urlpatterns = [
    path('kakao/', GetKakaoInfoAPIView.as_view(), name="kakao_login"),
    path('signup/', SignUpAPIView.as_view(), name="signup"),

    # path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
