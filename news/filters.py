import django_filters
from news.models import News


class NewsFilter(django_filters.FilterSet):
    class Meta:
        model = News
        fields = ("category",)
