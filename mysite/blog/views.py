from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.all()
    # 페이지당 3개의 게시물로 페이지 매김
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)  # paginator.page()는 strict한 방식이라 예외처리 필수
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, year: int, month: int, day: int, post: str) -> HttpResponse:
    post_obj = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post_obj})
