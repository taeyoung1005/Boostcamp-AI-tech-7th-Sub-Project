from django.contrib import admin
from .models import Question, Answer

# Register your models here.


class CustomQuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "created_at", "views_count", "is_deleted"]
    list_filter = ["created_at", "is_deleted"]
    search_fields = ["title", "content"]
    ordering = ["-created_at"]


class CustomAnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "question", "created_at", "is_deleted"]
    list_filter = ["created_at", "is_deleted"]
    search_fields = ["content"]
    ordering = ["-created_at"]


admin.site.register(Question, CustomQuestionAdmin)
admin.site.register(Answer, CustomAnswerAdmin)
