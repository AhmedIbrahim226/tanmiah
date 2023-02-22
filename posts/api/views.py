from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import UserAuth
from .serializers import (Post, PostSerializer, PostMedia, PostMediaSerializer, Album, AlbumSerializer,
                          AlbumPostMediaSerializer, Folder, FolderSerializer)


class PostAPI(ModelViewSet):
    http_method_names = ('get', 'post', 'delete')
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        owner = UserAuth.objects.get(id=self.kwargs.get('user_id'))
        queryset = Post.objects.filter(owner=owner)
        return queryset

class PostMediaAPI(ModelViewSet):
    http_method_names = ('delete',)
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaSerializer
    lookup_field = 'pk'

class AlbumAPI(ModelViewSet):
    http_method_names = ('get', 'post', 'delete')
    serializer_class = AlbumSerializer
    lookup_field = 'pk'

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        owner = UserAuth.objects.get(id=self.kwargs.get('user_id'))
        queryset = Album.objects.filter(owner=owner)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serial = self.get_serializer(queryset, many=True)
        return Response(serial.data)


class AlbumPostMediaAPI(ModelViewSet):
    http_method_names = ('get', 'post')
    serializer_class = AlbumPostMediaSerializer

    def get_queryset(self, *args, **kwargs):
        owner = UserAuth.objects.get(id=self.kwargs.get('user_id'))
        queryset = Post.objects.filter(owner=owner)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serial = self.get_serializer(queryset, many=True)
        return Response(serial.data)

    def create(self, request, *args, **kwargs):
        serial = self.get_serializer(data=request.data)
        serial.context.update(album_id=kwargs.get('album_id'))
        if serial.is_valid():
            serial.save()
            return Response(serial.data)
        return Response(serial.errors, 400)

class FolderAPI(ModelViewSet):
    http_method_names = ('get', 'post', 'delete')
    serializer_class = FolderSerializer
    lookup_field = 'pk'

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        owner = UserAuth.objects.get(id=self.kwargs.get('user_id'))
        queryset = Folder.objects.filter(owner=owner)
        return queryset


class SubFolderAPI(ModelViewSet):
    http_method_names = ('get', )
    serializer_class = FolderSerializer

    def get_queryset(self):
        parent_folder_id = self.kwargs.get('parent_folder_id')
        parent_folder = Folder.objects.get(pk=parent_folder_id)
        queryset = Folder.objects.filter(parent_folder=parent_folder).order_by('-created_at')
        return queryset

