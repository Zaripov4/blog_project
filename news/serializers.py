from rest_framework import serializers
from news.models import News, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'

        extra_kwargs = {
            'author': {
                'read_only': True
            },
            'views': {
                'read_only': True
            }
        }


class NewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            'id',
            'title',
        )
