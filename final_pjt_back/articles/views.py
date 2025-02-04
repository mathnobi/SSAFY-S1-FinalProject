from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from .serializers import (
    ArticleSerializer, 
    CommentSerializer, 
    ArticleListSerializer, 
    CommentListSerializer
)
from .models import Article, Comment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user)  # user_id는 현재 로그인된 유저
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':  # 게시글 수정
        if article.user_id != request.user:  # 작성자만 수정 가능
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # 게시글 삭제
        if article.user_id != request.user:  # 작성자만 삭제 가능
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response({'detail': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':  # 특정 게시글에 달린 댓글 조회
        comments = Comment.objects.filter(post_id=article)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':  # 댓글 생성
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user, post_id=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_detail(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post_id=article_pk)

    if request.method == 'PUT':  # 댓글 수정
        if comment.user_id != request.user:  # 작성자만 수정 가능
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # 댓글 삭제
        if comment.user_id != request.user:  # 작성자만 삭제 가능
            return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({'detail': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
