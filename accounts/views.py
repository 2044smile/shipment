import requests

from django.utils.crypto import get_random_string
from django.http import JsonResponse
from rest_framework.views import APIView 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User


class KakaoLoginView(APIView):
    access_token = openapi.Parameter('access_token', openapi.IN_QUERY, description="Send it to me from Frontend", required=True, type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_description="프론트엔드(POSTMAN) 토큰 전달", responses={200: 'Success'}, manual_parameters=[access_token])
    def get(self, request):
        kakao_access_token = request.GET.get("access_token", None)

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
            return JsonResponse({"error": f"카카오 서버와의 통신에 실패했습니다: {str(e)}"}, status=500)
        except ValueError as e:
            return JsonResponse({"error": f"카카오 서버의 응답을 JSON으로 파싱하는 중에 오류가 발생했습니다: {str(e)}"}, status=500)


        target = get_random_string(length=16, allowed_chars="가나다라마바사thankyousomuch")

        obj, created = User.objects.get_or_create(
            kakao_id=response_data['id'],
            kakao_nickname=response_data['properties']['nickname'],
            defaults={'username': target}
        )

        return JsonResponse({"kakao_id": f"{obj.kakao_id}", "kakao_nickname": f"{obj.kakao_nickname}", "usernmae": f"{obj.username}"})
