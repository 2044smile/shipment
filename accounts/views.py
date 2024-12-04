import requests

from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserSerializer


import requests

from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserSerializer


class KakaoAuthAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    access_token = openapi.Parameter('access_token', openapi.IN_QUERY, description="access_token", required=True, type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_id="회원가입/로그인", operation_description="카카오에서 전달 받은 액세스 토큰", responses={200: 'Success'}, manual_parameters=[access_token])
    def post(self, request):
        access_token = request.GET.get("access_token", None)

        if not access_token:
            return JsonResponse({"error": "카카오 액세스 토큰이 제공되지 않았습니다."}, status=400)

        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            kakao_id = response_data["id"]
            kakao_nickname = response_data['properties']['nickname']

            user, created = User.objects.get_or_create(
                user_id=kakao_id,
                kakao_id=kakao_id,
                kakao_nickname=kakao_nickname
            )

            if created:
                user.username = get_random_string(length=16, allowed_chars="가나다라마바사thankyousomuch")
                user.is_valid = True
                user.save()

        except requests.RequestException:
            return JsonResponse({"error": "카카오 서버와의 통신에 실패했습니다."}, status=500)
        except ValueError as e:
            return JsonResponse({"error": f"카카오 서버의 응답을 JSON으로 파싱하는 중에 오류가 발생했습니다: {str(e)}"}, status=500)

        token = TokenObtainPairSerializer.get_token(user)

        refresh_token = str(token)
        access_token = str(token.access_token)
        iat = token.get('iat', None)  # 토큰이 발급 된 시간
        exp = token.get('exp', None)  # 토큰 만료 시간

        return JsonResponse({
            "id": user.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "iat": iat,
            "exp": exp
        })
