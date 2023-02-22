from django.urls import path
from .views import (PostAPI, AlbumAPI, AlbumPostMediaAPI, FolderAPI, SubFolderAPI, PostMediaAPI)

urlpatterns = [
    path('<user_id>/', PostAPI.as_view({'get': 'list', 'post': 'create'})),
    path('<user_id>/delete/<pk>/', PostAPI.as_view({'delete': 'destroy'})),
    path('<user_id>/delete/media/<pk>/', PostMediaAPI.as_view({'delete': 'destroy'})),
    path('<user_id>/photos/albums/', AlbumAPI.as_view({'get': 'list', 'post': 'create'})),
    path('<user_id>/photos/albums/delete/<pk>/', AlbumAPI.as_view({'delete': 'destroy'})),
    path('<user_id>/photos/albums/<album_id>/', AlbumPostMediaAPI.as_view({'get': 'list', 'post': 'create'})),
    path('<user_id>/documents/', FolderAPI.as_view({'get': 'list', 'post': 'create'})),
    path('<user_id>/documents/delete/<pk>/', FolderAPI.as_view({'delete': 'destroy'})),
    path('<user_id>/documents/folders/<parent_folder_id>/', SubFolderAPI.as_view({'get': 'list'})),
]

