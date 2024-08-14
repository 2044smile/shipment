from rest_framework.permissions import BasePermission, SAFE_METHODS


class CannotPurchaseOwnProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 자체 제품을 구매할 수 없습니다.
        return obj.user != request.user