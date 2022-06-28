from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("news", views.NewViewSet)
router.register("comments", views.CommentViewSet)
router.register("category", views.CategoryViewSet)

urlpatterns = [path("", include(router.urls))]
