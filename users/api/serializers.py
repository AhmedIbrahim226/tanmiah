from rest_framework import serializers
from ..models import UserAuth, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('owner', )

class UserAuthSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    joined_in = serializers.ReadOnlyField(source='ret_naturalday_joined')
    class Meta:
        model = UserAuth
        fields = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_moderator', 'is_staff',
                  'is_superuser', 'is_user', 'user_permissions', 'groups', 'joined_in', 'profile')


    def create(self, validated_data):
        profile = validated_data.pop('profile')
        followers = profile.pop('followers')
        follow = profile.pop('follow')

        user_permissions = validated_data.pop('user_permissions')
        groups = validated_data.pop('groups')
        user = UserAuth.objects.create(**validated_data)
        user.user_permissions.set(user_permissions)
        user.user_permissions.set(groups)

        profile = UserProfile.objects.create(owner=user, **profile)
        profile.followers.set(followers)
        profile.followers.set(follow)

        return user
