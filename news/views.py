from django.views.generic import DetailView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import News, Comment, Category
from .serializers import (
    NewsSerializer,
    CommentSerializer,
    NewListSerializer,
    CategorySerializer,
)


class NewViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ("category__name", "author", "author__username")
    ordering = ("-category",)
    search_fields = (
        "title",
        "body",
    )
    ordering_fields = (
        "id",
        "title",
        "category",
    )

    def get_serializer_class(self):
        if self.action == "list":
            return NewListSerializer
        else:
            return NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.views += 1
        obj.save()
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def NewsLike(request, pk):
    post = get_object_or_404(
        News,
    )
    if post.like.filter(id=request.user.id).exist():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return HttpResponseRedirect(reverse("news_detail", args=[str(pk)]))


def NewsDislike(request, pk):
    post = get_object_or_404(
        News,
    )
    if post.dislike.filter(id=request.user.id).exists():
        post.dislike.remove(request.user)
    else:
        post.dislike.add(request.user)

    return HttpResponseRedirect(reverse("news_detail", args=str(pk)))


class NewsDetailView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        like_connected = get_object_or_404(News, id=self.kwargs["pk"])
        liked = False
        if like_connected.like.filter(id=self.request.user.id).exists():
            liked = True
        data["number_of_likes"] = like_connected.number_of_likes()
        data["post_is_liked"] = liked
        return data


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
