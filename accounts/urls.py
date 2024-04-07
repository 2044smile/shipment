from django.urls import path
from accounts.views import KakaoSignInAPIView, KakaoSignUpAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name = 'accounts'

urlpatterns = [
    path('signup/', KakaoSignUpAPIView.as_view(), name="signup"),
    path('signin/', KakaoSignInAPIView.as_view(), name="signin"),

    # path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
