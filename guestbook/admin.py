from django.contrib import admin

from .models import GuestBook


class GuestBookAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "content",
        "created_at",
        "updated_at",
        "is_deleted",
        "ip_address",
    ]
    list_filter = ["is_deleted"]
    search_fields = ["author", "content"]


admin.site.register(GuestBook, GuestBookAdmin)
