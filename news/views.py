from rest_framework import viewsets
from .models import News, Comment, Category
from .serializers import NewsSerializer, CommentSerializer, NewListSerializer, CategorySerializer


class NewViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_serializer_class(self):
        if self.action == 'list':
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


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
