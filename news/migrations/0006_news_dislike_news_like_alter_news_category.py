# Generated by Django 4.0.5 on 2022-06-28 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_category_alter_news_author_alter_news_views_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='dislike',
            field=models.ManyToManyField(
                related_name='news_dislike', to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='news',
            name='like',
            field=models.ManyToManyField(
                related_name='news_like', to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='news',
                to='news.category',
            ),
        ),
    ]
