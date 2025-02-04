from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('comment_id', 'content')

    # comment_set 역참조 데이터를 커스터마이징
    comment_set = CommentDetailSerializer(read_only=True, many=True)
    # 댓글 개수를 제공하는 필드
    number_of_comments = serializers.IntegerField(source='comment_set.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user_id',)


class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('post_id', 'title')

    # `article` 필드를 게시글 제목으로 커스터마이징
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user_id', 'post_id')


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('post_id', 'title', 'content')

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_id', 'content', 'user_id')