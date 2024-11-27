from django.db import models


class GuestBook(models.Model):
    author = models.CharField(max_length=30, default="Anonymous")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return self.author
