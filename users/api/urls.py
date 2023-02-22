from django.urls import path
from .views import (UserAuthAPI)

urlpatterns = [
    path('', UserAuthAPI.as_view({'get': 'list', 'post': 'create'})),
]
