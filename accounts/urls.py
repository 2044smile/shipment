from django.urls import path
from accounts.views import KakaoAuthAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = 'accounts'

urlpatterns = [
    path('auth/', KakaoAuthAPIView.as_view(), name="signin"),

    # path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
