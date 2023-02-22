from rest_framework import serializers
from ..models import Post, Album, PostMedia, Folder
from ..validators import image_filed_validator
from django.shortcuts import get_object_or_404


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('post', 'album', 'folder', 'img', 'video', 'document')

class PostSerializer(serializers.ModelSerializer):
    post_media = PostMediaSerializer(many=True, required=False)

    _privacy = serializers.ReadOnlyField(source='get_privacy_str', read_only=True)
    created_at = serializers.ReadOnlyField(source='ret_naturaltime_created', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'owner', 'privacy', '_privacy', 'media', 'description', 'share_with',
            'created_at', 'post_media')
        extra_kwargs = {
            'media': {'write_only': True},
            'privacy': {'write_only': True},
        }


    def validate(self, attrs):
        media = attrs.get('media')
        post_media_list = self.initial_data.getlist('post_media', [])
        folder_id = self.initial_data.get('folder_id', None)

        if media != 4:
            media_type = None
            folder = None
            if media == 1:
                """
                # validate image sizing
                for img in native_post_media:
                    image_filed_validator(img)
                """
                media_type = 'img'
            elif media == 2:
                media_type = 'video'
            elif media == 3:
                if folder_id:
                    folder = Folder.objects.get(pk=folder_id)
                    attrs['privacy'] = folder.privacy
                media_type = 'document'

            attrs['post_media'] = [{media_type: media, 'folder': folder} for media in post_media_list]

        return attrs

    def validate_media(self, value):
        post_media = self.initial_data.get('post_media', None)
        if value != 4 and not post_media:
            raise serializers.ValidationError('In case you defined type of media, you must include media.')
        return value


    def create(self, validated_data):
        post_media = validated_data.pop('post_media', [])
        share_with = validated_data.pop('share_with', [])

        post = Post.objects.create(**validated_data)
        post.share_with.add(*share_with)

        for media in post_media:
            PostMedia.objects.create(post=post, **media)
        return post


class AlbumSerializer(serializers.ModelSerializer):
    post_media = PostMediaSerializer(many=True, required=False)
    _privacy = serializers.ReadOnlyField(source='get_privacy_str')
    created_at = serializers.ReadOnlyField(source='ret_naturalday_created')

    class Meta:
        model = Album
        fields = ('id', 'owner', 'name', 'privacy', '_privacy', 'created_at', 'post_media')
        extra_kwargs = {
            'privacy': {'write_only': True},
        }

    def validate(self, attrs):
        native_post_medias = self.initial_data.getlist('post_media', [])

        if native_post_medias:
            """
            # validate image sizing
            for img in native_album_album_photos:
                image_filed_validator(img)
            """
            attrs['post_media'] = [{"img": photo} for photo in native_post_medias]

        return attrs

    def create(self, validated_data):
        album_media = validated_data.pop('post_media', [])

        album = Album.objects.create(**validated_data)

        for media in album_media:
            PostMedia.objects.create(album=album, **media)
        return album

class AlbumPostMediaSerializer(serializers.ModelSerializer):
    post_media = PostMediaSerializer(many=True, required=False)

    _privacy = serializers.ReadOnlyField(source='get_privacy_str', read_only=True)
    created_at = serializers.ReadOnlyField(source='ret_naturaltime_created', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'owner', '_privacy', 'media', 'description', 'share_with', 'created_at', 'post_media')
        extra_kwargs = {
            'media': {'write_only': True},
        }

    def validate(self, attrs):
        album_id = self.context.get('album_id')
        album = get_object_or_404(Album, pk=album_id)
        attrs['album'] = album
        media = attrs.get('media')
        post_media_list = self.initial_data.getlist('post_media', [])

        if media != 4:
            media_type = None
            if media == 1:
                """
                # validate image sizing
                for img in native_post_media:
                    image_filed_validator(img)
                """
                media_type = 'img'
            elif media == 2:
                media_type = 'video'
            elif media == 3:
                media_type = 'document'

            attrs['post_media'] = [{media_type: media} for media in post_media_list]
        return attrs

    def validate_media(self, value):
        post_media = self.initial_data.get('post_media', None)
        if value != 4 and not post_media:
            raise serializers.ValidationError('In case you defined type of media, you must include media.')
        return value

    def create(self, validated_data):
        post_media = validated_data.pop('post_media', [])
        share_with = validated_data.pop('share_with', [])
        album = validated_data.pop('album', None)
        album_privacy = album.privacy

        post = Post.objects.create(privacy=album_privacy, **validated_data)
        post.share_with.add(*share_with)

        for media in post_media:
            PostMedia.objects.create(post=post, album=album, **media)
        return post


class FolderSerializer(serializers.ModelSerializer):
    _privacy = serializers.ReadOnlyField(source='get_privacy_str')
    created_at = serializers.ReadOnlyField(source='ret_naturalday_created')

    class Meta:
        model = Folder
        fields = ('id', 'name', 'privacy', 'parent_folder', '_privacy', 'created_at', 'owner')
        extra_kwargs = {
            'privacy': {'write_only': True},
        }


    def validate(self, attrs):
        parent_folder = attrs.get('parent_folder')

        if parent_folder:
            privacy = parent_folder.privacy
            attrs.update(privacy=privacy)
        return attrs
