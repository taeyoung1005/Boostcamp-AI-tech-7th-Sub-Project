from django.contrib import admin

from .models import ClassificationImage


class ClassificationImageAdmin(admin.ModelAdmin):
    list_display = ["user", "classification_image", "prediction", "created_at"]
    search_fields = ["user__username", "classification_image", "prediction"]
    list_filter = ["created_at"]


admin.site.register(ClassificationImage, ClassificationImageAdmin)
