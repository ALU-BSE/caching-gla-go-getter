from django.conf import settings
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def _invalidate_users_list_cache(self):
        cache_key = "users_list"
        cache.delete(cache_key)

    def list(self, request, *args, **kwargs):
        cache_key = "users_list"
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response

    def create(self, request, *args, **kwargs):
        self._invalidate_users_list_cache()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._invalidate_users_list_cache()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._invalidate_users_list_cache()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._invalidate_users_list_cache()
        return super().destroy(request, *args, **kwargs)