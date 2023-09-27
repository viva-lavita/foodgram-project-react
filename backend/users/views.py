from api.pagination import LimitPageNumberPagination
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import UserFollowSerializer

User = get_user_model()


class UserFollowViewSet(UserViewSet):
    """Вьюсет создания и удаления подписки."""
    http_method_names = ['get', 'post', 'delete']
    pagination_class = LimitPageNumberPagination

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserFollowSerializer(page,
                                              many=True,
                                              context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = UserFollowSerializer(author,
                                              data=request.data,
                                              context={'request': request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user,
                                  author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(Follow,
                                         user=user,
                                         author=author)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()
