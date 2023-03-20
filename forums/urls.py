from django.urls import path
from .views import ForumsView, DiscussionListView, DiscussionCreateView, DiscussionDetailView, DiscussionListViewByTag


urlpatterns = [
    path(
        "",
        ForumsView.as_view(),
        name="forums_view"
    ),
    path(
        "<int:forum_id>/discussions/",
        DiscussionListView.as_view(),
        name='discussion_list_view'
    ),
    path(
        '<int:forum_id>/new/discussion/',
        DiscussionCreateView.as_view(),
        name='new_discussion_view'
    ),
    path(
        'discussions/<discussion_id>/',
        DiscussionDetailView.as_view(),
        name='discussion_detail_view'
    ),
    path(
        "discussions/tagged/<tag_slug>",
        DiscussionListViewByTag.as_view(),
        name='discussion_tag_list_view'
    ),
    
]
