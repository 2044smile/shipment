import requests

from django.utils.crypto import get_random_string
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import UserSerializer


class GetKakaoInfoAPIView(APIView):
    kakao_access_token = openapi.Parameter('kakao_access_token', openapi.IN_QUERY, description="Send it to me from Frontend", required=True, type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_description="프론트엔드(POSTMAN) 토큰 전달", responses={200: 'Success'}, manual_parameters=[kakao_access_token])
    def get(self, request):
        kakao_access_token = request.GET.get("kakao_access_token", None)

        if not kakao_access_token:
            return JsonResponse({"error": "카카오 액세스 토큰이 제공되지 않았습니다."}, status=400)

        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {kakao_access_token}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
        except requests.RequestException:
            return JsonResponse({"error": "카카오 서버와의 통신에 실패했습니다."}, status=500)
        except ValueError as e:
            return JsonResponse({"error": f"카카오 서버의 응답을 JSON으로 파싱하는 중에 오류가 발생했습니다: {str(e)}"}, status=500)

        return JsonResponse({"kakao_id": f"{response_data['id']}", "kakao_nickname": f"{response_data['properties']['nickname']}"})
    
    
class SignUpAPIView(APIView):
    @swagger_auto_schema(operation_description="회원가입", responses={200: 'Success'}, request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'kakao_access_token': openapi.Schema(type=openapi.TYPE_STRING, description='kakao_access token'),  # 회원가입 Kakao Access Token 사용
                'kakao_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='kakao id'),
                'kakao_nickname': openapi.Schema(type=openapi.TYPE_STRING, description='kakao nickname'),
            }
    ))
    def post(self, request):
        serializer = UserSerializer(data={
            "kakao_access_token": request.data['kakao_access_token'],
            "kakao_id": request.data['kakao_id'],
            "kakao_nickname": request.data['kakao_nickname'],
            "user_id": request.data['kakao_id']
        })
        if serializer.is_valid():
            request = requests.get(url='https://kapi.kakao.com/v1/user/access_token_info', params={'access_token': request.data.get('kakao_access_token')})
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
                'kakao_id': user.kakao_id,
                'access_token': access_token, 
                'refresh_token': refresh_token,
                'iat': iat,
                'exp': exp,
                
            })  # jwt token 발급
        else:
            return JsonResponse({'errors': '중복 데이터가 존재합니다.', 'details': f"{serializer.errors}"}, status=400)


class SignInAPIView(APIView):
    @swagger_auto_schema(operation_description="로그인", responses={200: 'Success'}, request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='access token'),  # 로그인 jwt Access Token 사용'
                'kakao_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='kakao id'),
                'kakao_nickname': openapi.Schema(type=openapi.TYPE_STRING, description='kakao nickname'),
            }
    ))
    def post(self, request):
        # 프론트엔드에서는 Access Token 과 유저의 개인정보를 가지고 있다는 가정
        data = {}
        try:
            user = User.objects.get(kakao_id=request.data.get("kakao_id", None))
            if user is None:
                return JsonResponse({'errors': '유저가 존재하지 않습니다.'}, status=400)
            
            response = requests.post('http://localhost:8000/accounts/token/verify/', data={'token': request.data.get("access_token")})
            if response.status_code != 200:
                return JsonResponse({'errors': '토큰이 유효하지 않습니다.'}, status=400)
            
            data['access_token'] = request.data.get("access_token")
            data['kakao_id'] = request.data.get("kakao_id")
            data['kakao_nickname'] = request.data.get("kakao_nickname")
            
            return Response(data, status=status.HTTP_200_OK)
            
        except:
            pass
