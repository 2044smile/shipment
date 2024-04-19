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


class KakaoSignInAPIView(APIView):
    # @swagger_auto_schema(operation_description="회원가입", responses={200: 'Success'}, request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='access token'),  # 회원가입 Kakao Access Token 사용
    #             'kakao_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='kakao id'),
    #             'kakao_nickname': openapi.Schema(type=openapi.TYPE_STRING, description='kakao nickname'),
    #         }
    # ))
    permission_classes = [permissions.AllowAny]

    access_token = openapi.Parameter('access_token', openapi.IN_QUERY, description="access_token", required=True, type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_description="카카오에서 전달받은 액세스 토큰", responses={200: 'Success'}, manual_parameters=[access_token])
    def post(self, request):
        access_token = request.GET.get("access_token", None)  # 카카오에서 전달받은 액세스 토큰

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

            user = User.objects.get(kakao_id=kakao_id, kakao_nickname=kakao_nickname)
        except requests.RequestException:
            return JsonResponse({"error": "카카오 서버와의 통신에 실패했습니다."}, status=500)
        except ValueError as e:
            return JsonResponse({"error": f"카카오 서버의 응답을 JSON으로 파싱하는 중에 오류가 발생했습니다: {str(e)}"}, status=500)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "SHIPMENT 회원가입이 되어 있지 않습니다."})
        
        request = requests.get(url='https://kapi.kakao.com/v1/user/access_token_info', params={'access_token': access_token})
        if request.status_code != 200:
            return JsonResponse({"error": f"카카오 Access Token 이 유효하지 않습니다.: {request.status_code}"}, status=int(request.status_code))
        
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
    
    
class KakaoSignUpAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    access_token = openapi.Parameter('access_token', openapi.IN_QUERY, description="access_token", required=True, type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_description="회원가입", responses={200: 'Success'}, manual_parameters=[access_token])
    def post(self, request):
        access_token = request.GET.get("access_token", None)  # 카카오에서 전달받은 액세스 토큰
        if not access_token:
            return JsonResponse({"error": "카카오 액세스 토큰이 제공되지 않았습니다."}, status=400)

        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        response = requests.post(url, headers=headers)

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()

            kakao_id = response_data["id"]
            kakao_nickname = response_data['properties']['nickname']
        except requests.RequestException:
            return JsonResponse({"error": "카카오 서버와의 통신에 실패했습니다."}, status=500)
        except ValueError as e:
            return JsonResponse({"error": f"카카오 서버의 응답을 JSON으로 파싱하는 중에 오류가 발생했습니다: {str(e)}"}, status=500)

        serializer = UserSerializer(data={
            "access_token": access_token,
            "kakao_id": kakao_id,
            "kakao_nickname": kakao_nickname,
            "user_id": kakao_id
        })
        if serializer.is_valid():
            request = requests.get(url='https://kapi.kakao.com/v1/user/access_token_info', params={'access_token': access_token})
            if request.status_code != 200:
                return JsonResponse({"error": f"카카오 Access Token 이 유효하지 않습니다.: {request.status_code}"}, status=int(request.status_code))
            user = serializer.save()

            token = TokenObtainPairSerializer.get_token(user)

            refresh_token = str(token)
            access_token = str(token.access_token)
            iat = token.get('iat', None)  # 토큰이 발급 된 시간
            exp = token.get('exp', None)  # 토큰 만료 시간

            target = get_random_string(length=16, allowed_chars="가나다라마바사thankyousomuch")

            if user.username is True:
                user.is_valid = True
            else:
                user.username = target
                user.is_valid = True

            user.save()

            return JsonResponse({
                'id': user.id,
                'kakao_id': user.kakao_id,
                'access_token': access_token, 
                'refresh_token': refresh_token,
                'iat': iat,
                'exp': exp,
            })  # jwt token 발급
        else:
            return JsonResponse({'errors': '중복 데이터가 존재합니다.', 'details': f"{serializer.errors}"}, status=400)
