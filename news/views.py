from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .forms import CommentForm
from .models import News
from .serializers import NewsSerializer
from django.shortcuts import render, get_object_or_404


class NewViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]


def post_detail(request, slug):
    post = get_object_or_404(News, slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save()
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()

        return render(request, {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
        })
