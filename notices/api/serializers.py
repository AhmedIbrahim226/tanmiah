from rest_framework import serializers
from ..models import ForumNotice



class ForumNoticeSerializer(serializers.ModelSerializer):
    _created_at = serializers.ReadOnlyField(source='ret_created_at')
    href = serializers.ReadOnlyField(source='get_notice_href')
    class Meta:
        model = ForumNotice
        fields = ('content', 'href', 'is_read', '_created_at')