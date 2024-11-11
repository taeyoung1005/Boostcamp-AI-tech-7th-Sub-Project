from django.db import models
from account.models import User


class Feedback(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Feedbacks")
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)  # 조회수 필드 추가
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
