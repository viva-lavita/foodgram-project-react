from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)

from .models import Follow
from .serializers import FollowSerializer, UserFollowSerializer


User = get_user_model()


class UserFollowViewSet(GenericViewSet, ListModelMixin):
    serializer_class = UserFollowSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.follower)


class FollowViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        author=self.kwargs['author_id'])
