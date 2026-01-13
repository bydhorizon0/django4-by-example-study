from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models.aggregates import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag

from blog.forms import EmailForm, CommentForm, SearchForm
from blog.models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_list(request: HttpRequest, tag_slug=None) -> HttpResponse:
    all_posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
    # 페이지당 3개의 게시물로 페이지 매김
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)  # paginator.page()는 strict한 방식이라 예외처리 필수
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


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
    # 사용자가 댓글을 달 수 있는 폼
    form = CommentForm()
    # 유사한 게시물들의 목록
    post_tags_ids = post_obj.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post_obj.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    return render(
        request,
        "blog/post/detail.html",
        {"post": post_obj, "comments": comments, "form": form, "similar_posts": similar_posts},
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


def post_search(request: HttpRequest):
    form = SearchForm()
    query = None
    results = []

    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = Post.published.annotate(search=SearchVector("title", "content")).filter(
                search=query
            )

    return render(
        request, "blog/post/search.html", {"form": form, "query": query, "results": results}
    )
