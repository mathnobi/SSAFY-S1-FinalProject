from django.db import models
from accounts.models import User
from django.conf import settings

# Create your models here.
class Article(models.Model):
    post_id = models.AutoField(primary_key=True, unique=True)                           # 게시글 아이디 (자동 생성)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)   # 유저 아이디 (외래키)
    title = models.CharField(max_length=100)                                            # 제목
    content = models.TextField()                                                        # 내용
    created_at = models.DateTimeField(auto_now_add=True)                                # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)                                    # 수정 시간

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True, unique=True)                            # 댓글 아이디 (자동 생성)   
    user_id  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments') # 유저 아이디 (외래키)
    post_id = models.ForeignKey(Article, on_delete=models.CASCADE)                                    # 게시글 아이디 (외래키)
    content = models.TextField()                                                                      # 내용
    created_at = models.DateTimeField(auto_now_add=True)                                              # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)                                                  # 수정 시간