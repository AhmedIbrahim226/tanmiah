from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ForumFile, ForumFileSerializer, DiscussionVoteSerializer, DiscussionComment,
                          DiscussionCommentSerializer, Answer, AnswerSerializer, AnswerComment, AnswerCommentSerializer)
from ..models import Discussion


class ForumFileAPI(CreateAPIView):
    serializer_class = ForumFileSerializer
    queryset = ForumFile


class DiscussionVoteAPI(APIView):
    http_method_names = ('post',)

    def get_object(self):
        instance = Discussion.objects.get(id=self.kwargs.get('id'))
        return instance

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serial = DiscussionVoteSerializer(data=request.data)
        if serial.is_valid():
            if request.user != instance.author:
                if serial.validated_data.get('vote_type') == '+':
                    instance.vote.add(request.user)
                elif serial.validated_data.get('vote_type') == '-':
                    instance.vote.remove(request.user)
                return Response(serial.data, 200)
            return Response({'failure': 'User can\'t vote for him self!'}, 400)

        return Response(serial.errors)


class DiscussionCommentAPI(CreateAPIView):
    serializer_class = DiscussionCommentSerializer
    queryset = DiscussionComment

    def create(self, request, *args, **kwargs):
        if request.user.has_perm('forums.denied_to_add_safe_discussion') and not request.user.is_superuser:
            request.data['safe'] = False
        return super().create(request, args, kwargs)


class AnswerAPI(CreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer

    def create(self, request, *args, **kwargs):
        if request.user.has_perm('forums.denied_to_add_safe_answer') and not request.user.is_superuser:
            request.data['safe'] = False
        return super().create(request, args, kwargs)


class AnswerVoteAPI(APIView):
    http_method_names = ('post',)

    def get_object(self):
        instance = Answer.objects.get(id=self.kwargs.get('id'))
        return instance

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serial = DiscussionVoteSerializer(data=request.data)
        if serial.is_valid():
            if request.user != instance.author:
                if serial.validated_data.get('vote_type') == '+':
                    instance.vote.add(request.user)
                elif serial.validated_data.get('vote_type') == '-':
                    instance.vote.remove(request.user)
                return Response(serial.data, 200)
            return Response({'failure': 'User can\'t vote for him self!'}, 400)

        return Response(serial.errors)


class AnswerCommentAPI(CreateAPIView):
    serializer_class = AnswerCommentSerializer
    queryset = AnswerComment

    def create(self, request, *args, **kwargs):
        if request.user.has_perm('forums.denied_to_add_safe_answer_comment') and not request.user.is_superuser:
            request.data['safe'] = False
        return super().create(request, args, kwargs)
