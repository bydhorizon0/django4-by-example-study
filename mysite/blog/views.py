from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from blog.forms import EmailForm, CommentForm
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
    comments = post_obj.comments.all()
    form = CommentForm()
    return render(
        request, "blog/post/detail.html", {"post": post_obj, "comments": comments, "form": form}
    )


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    # id로 게시물 조회
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            # 유효성 검사를 통과한 폼 필드들
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                rf"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, "bydhorizon0@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailForm()
    context = {"post": post, "form": form, "sent": sent}
    return render(request, "blog/post/share.html", context)


@require_POST
def post_comment(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request, "blog/post/comment.html", {"comment": comment, "post": post, "form": form}
    )
