from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from users.models import UserAuth
from .serializers import (ForumFile, ForumFileSerializer, Discussion, DiscussionVoteSerializer, DiscussionComment, DiscussionCommentSerializer, Answer, AnswerSerializer, AnswerComment, AnswerCommentSerializer)
from rest_framework.response import Response
from django.db.models import F

class ForumFileAPI(CreateAPIView):
    serializer_class = ForumFileSerializer
    queryset = ForumFile
    

class DiscussionVoteAPI(APIView):
    http_method_names = ('post')

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


class AnswerAPI(CreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer

class AnswerVoteAPI(APIView):
    http_method_names = ('post')

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
    