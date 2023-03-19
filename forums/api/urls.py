from django.urls import path
from .views import ForumFileAPI, DiscussionVoteAPI, DiscussionCommentAPI, AnswerAPI, AnswerVoteAPI, AnswerCommentAPI


urlpatterns = [
    path("forum/file/", ForumFileAPI.as_view()),
    path("forum/discussion/<id>/vote/", DiscussionVoteAPI.as_view()),
    path("forum/discussion/comment/", DiscussionCommentAPI.as_view()),
    path("forum/answer/", AnswerAPI.as_view()),
    path("forum/answer/<id>/vote/", AnswerVoteAPI.as_view()),
    path("forum/answer/comment/", AnswerCommentAPI.as_view()),
]
