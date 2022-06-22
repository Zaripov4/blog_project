from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import News
from .serializers import NewsSerializer


class NewViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
