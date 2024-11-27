from django.shortcuts import render
from django.core.paginator import Paginator

from .models import GuestBook


def get_client_ip(request):
    """
    Get client IP address from the request.
    Supports proxy setups using `X-Forwarded-For`.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # Use the first IP in the list
    else:
        ip = request.META.get("REMOTE_ADDR")  # Fallback to REMOTE_ADDR
    return ip


def comment_list(request):
    if request.method == "POST":
        author = request.POST.get("author")
        if author == "":
            author = "Anonymous"

        content = request.POST.get("content")
        ip_address = get_client_ip(request)
        if content:
            guestbook = GuestBook(author=author, content=content, ip_address=ip_address)
            guestbook.save()

    guestbooks = GuestBook.objects.filter(is_deleted=False).order_by("-created_at")

    paginator = Paginator(guestbooks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "guestbook/guestbook.html", {"page_obj": page_obj})
