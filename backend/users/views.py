from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action

from .serializers import UserFollowSerializer


User = get_user_model()


class UserFollowViewSet(UserViewSet):

    @action(detail=False)
    def subscriptions(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserFollowSerializer(page,
                                              many=True,
                                              context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, id=None):
        serializer = UserFollowSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data