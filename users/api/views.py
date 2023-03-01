from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .serializers import (UserAuthSerializer, UserAuth)


class UserAuthAPI(ModelViewSet):
    http_method_names = ('get', 'post')
    serializer_class = UserAuthSerializer

    def get_queryset(self):
        return UserAuth.objects.exclude(id=self.request.user.id)
