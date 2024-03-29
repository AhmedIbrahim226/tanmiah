from rest_framework import serializers

from ..models import ForumFile, DiscussionComment, Answer, AnswerComment


class ForumFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumFile
        fields = '__all__'


class DiscussionVoteSerializer(serializers.Serializer):
    vote_type = serializers.CharField(required=True)


class DiscussionCommentSerializer(serializers.ModelSerializer):
    at = serializers.ReadOnlyField(source='ret_created')

    class Meta:
        model = DiscussionComment
        fields = ('author', 'discussion', 'content', 'safe', 'at')


class AnswerSerializer(serializers.ModelSerializer):
    at = serializers.ReadOnlyField(source='ret_created_at')

    class Meta:
        model = Answer
        fields = ('author', 'discussion', 'content', 'at')


class AnswerCommentSerializer(serializers.ModelSerializer):
    at = serializers.ReadOnlyField(source='ret_created')

    class Meta:
        model = AnswerComment
        fields = ('author', 'answer', 'content', 'at')
