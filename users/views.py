from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, CreateView
from django.contrib.auth.views import LoginView
from .models import UserAuth, UserProfile
from posts.models import Post, PostMedia, Folder
from .forms import (LoginForm, UserRegisterForm)
from django.db.models import Q
from itertools import chain
from django.utils.decorators import method_decorator


class TanmiahHome(TemplateView):
    template_name = 'users/tanmiah_home.html'


class UserLoginView(LoginView):
    form_class = LoginForm


class UserRegisterView(CreateView, FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user_registration_succeed')


class RegistrationSucceed(TemplateView):
    template_name = 'users/registration_succeed.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class UserTimelineView(LoginRequiredMixin, TemplateView):
    """"""
    template_name = 'users/timeline.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.request.user.posts.all().order_by('-created_at')
        context.update({'posts': posts})
        return context


class UserPhotosView(LoginRequiredMixin, TemplateView):
    template_name = 'users/photos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_photos = PostMedia.objects.filter(
            Q(post__owner=self.request.user) | Q(album__owner=self.request.user)).order_by('-created_at')
        context.update(user_photos=user_photos)
        return context


class UserAlbumsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(user_albums=self.request.user.albums.all().order_by('-created_at'))
        return context


class UserAlbumDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'users/album_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_album = self.request.user.albums.get(pk=kwargs.get('album_id'))
        album_media = user_album.album_media.all().order_by('-created_at')
        context.update(user_album=user_album)
        context.update(user_album_details=album_media)
        return context


class UserVideosView(LoginRequiredMixin, TemplateView):
    template_name = 'users/videos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_videos = PostMedia.objects.filter(
            Q(post__owner=self.request.user) | Q(album__owner=self.request.user)).order_by('-created_at')
        context.update(user_videos=user_videos)
        return context


class UserDocsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/documents.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_docs_files = PostMedia.objects.filter(post__owner=self.request.user, folder__isnull=True, img__exact='',
                                             video__exact='', document__isnull=False)
        user_folders = self.request.user.folders.filter(parent_folder__isnull=True)

        user_doc_contents = sorted(chain(user_docs_files, user_folders), key=lambda k: k.created_at)
        context.update(user_doc_contents=user_doc_contents[::-1])

        return context

class UserDocsFolderView(LoginRequiredMixin, TemplateView):
    template_name = 'users/document_folder.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        folder = Folder.objects.prefetch_related('sub_folder').get(pk=kwargs.get('folder_id'))
        sub_folders = folder.sub_folder.all()
        folder_media_docs = PostMedia.objects.filter(folder=folder)

        folder_doc_contents = sorted(chain(sub_folders, folder_media_docs), key=lambda k: k.created_at)
        last_ordering = reversed(folder_doc_contents)
        context.update(folder_doc_contents=last_ordering)

        return context
