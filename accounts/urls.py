from django.urls import path
from accounts.views import AccountKakaoView, AccountKakaoCallBackView # , AccountSigninView, AccountSignoutView, AccountSignupView


urlpatterns = [
    path('kakao/callback', AccountKakaoCallBackView.as_view(), name="kakao_callback"),
    path('kakao/', AccountKakaoView.as_view(), name="kakao_login"),

    # path('signup/', AccountSignupView.as_view(), name="signup"),
    # path('signin/', AccountSigninView.as_view(), name="signin"),
    # path('signout/', AccountSignoutView.as_view(), name="signout")
]
