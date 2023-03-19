from ..models import ForumFile, Discussion, DiscussionComment, Answer, AnswerComment
from rest_framework import serializers


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
        fields = ('author', 'discussion', 'content', 'at')



class AnswerSerializer(serializers.ModelSerializer):
    at = serializers.ReadOnlyField(source='ret_created_at')
    class Meta:
        model = Answer
        fields = ('author', 'discussion','content', 'at')
    
    
    def create(self, validated_data):
        print(validated_data)
        answer = Answer.objects.create(**validated_data)

        discussion = answer.discussion
        discussion.time_case = 2
        discussion.at_date_time = answer.created_at
        discussion.save()

        return answer

class AnswerCommentSerializer(serializers.ModelSerializer):
    at = serializers.ReadOnlyField(source='ret_created')
    class Meta:
        model = AnswerComment
        fields = ('author', 'answer', 'content', 'at')