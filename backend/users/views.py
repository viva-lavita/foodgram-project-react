from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import response, status
from rest_framework.decorators import action

from .models import Follow
from .serializers import UserFollowSerializer


User = get_user_model()


class UserFollowViewSet(UserViewSet):
    """Вьюсет создания и удаления подписки."""
    http_method_names = ['get', 'post', 'delete']

    @action(detail=False)
    def subscriptions(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserFollowSerializer(page,
                                              many=True,
                                              context={'request': request})
            return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
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
            return response.Response(serializer.data,
                                     status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(Follow,
                                         user=user,
                                         author=author)
            self.perform_destroy(instance)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
