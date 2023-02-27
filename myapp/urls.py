from django.urls import path
from rest_framework import routers

from . import views

# Add funtion based view URLs here
urlpatterns = [
    path("hello/", views.hello),
]

# Add class based view URLs here
router = routers.SimpleRouter()
router.register("myapp", views.MyModelViewSet, basename="myapp")
urlpatterns += router.urls
