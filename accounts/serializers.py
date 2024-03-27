from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        # fields = ['kakao_id', 'kakao_nickname']

    # def create(self, validated_data):
    #     kakao_id = validated_data.get('kakao_id', None)
    #     kakao_nickname = validated_data.get('kakao_nickname', None)

    #     user = User(
    #         kakao_id=kakao_id,
    #         kakao_nickname=kakao_nickname
    #     )
    #     user.save()

    #     return user
