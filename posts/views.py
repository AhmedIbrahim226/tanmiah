from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, View
from .models import Post
from django import forms


class PostView(ListView):
    template_name = 'posts/posts.html'
    model = Post
