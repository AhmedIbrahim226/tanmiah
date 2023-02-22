from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import urls
from .views import (TanmiahHome, UserLoginView, UserRegisterView, RegistrationSucceed, UserTimelineView, UserPhotosView,
                    UserAlbumsView, UserAlbumDetailView, UserVideosView, UserDocsView, UserDocsFolderView)

urlpatterns = [
    path('', TanmiahHome.as_view(), name='tanmiah_home'),
    path("login/", UserLoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('register/succeed/', RegistrationSucceed.as_view(), name='user_registration_succeed'),
    path('members/<user_pk>/', UserTimelineView.as_view(), name='user_timeline'),
    path('members/<user_pk>/photos/', UserPhotosView.as_view(), name='user_photos'),
    path('members/<user_pk>/photos/albums/', UserAlbumsView.as_view(), name='user_albums'),
    path('members/<user_pk>/photos/albums/<album_id>/', UserAlbumDetailView.as_view(), name='user_album_detail'),
    path('members/<user_pk>/videos/', UserVideosView.as_view(), name='user_videos'),
    path('members/<user_pk>/documents/', UserDocsView.as_view(), name='user_docs'),
    path('members/<user_pk>/document/folders/<folder_id>/', UserDocsFolderView.as_view(), name='user_doc_folder'),
]
