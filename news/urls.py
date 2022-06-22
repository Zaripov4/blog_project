from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.NewViewSet)


urlpatterns = [
    path('news/', include(router.urls))
]
