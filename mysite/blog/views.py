from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=id)
    return render(request, "blog/post/detail.html", {"post": post})
