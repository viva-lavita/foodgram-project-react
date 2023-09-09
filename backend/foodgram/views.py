from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)

from .models import Recipe, Follow
from .serializers import (
    RecipeSerializer
)


# User = get_user_model()


# class UserFollowViewSet(GenericViewSet, ListModelMixin):
#     serializer_class = UserFollowSerializer

#     def get_queryset(self):
#         return User.objects.filter(following__user=self.request.user)


# class FollowViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin):
#     """Вьюсет создания и удаления подписки."""
#     serializer_class = FollowSerializer

#     def get_queryset(self):
#         return get_object_or_404(Follow, user=self.request.user, author_id=self.kwargs['pk'])

#     def perform_create(self, serializer):
#         author = get_object_or_404(User, id=self.kwargs['pk'])
#         serializer.save(user=self.request.user,
#                         author=author)

#     def destroy(self, request, *args, **kwargs):
#         if self.kwargs['pk'] == self.request.user.id:
#             return response.Response({
#                 'errors': 'Вы не можете отписаться от самого себя'
#             }, status=status.HTTP_400_BAD_REQUEST)
#         instance = get_object_or_404(Follow, author_id=self.kwargs['pk'], user=self.request.user)
#         self.perform_destroy(instance)
#         return response.Response(status=status.HTTP_204_NO_CONTENT)





class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
