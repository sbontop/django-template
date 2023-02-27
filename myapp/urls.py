from django.urls import path
from rest_framework import routers

from . import views

# Add funtion based view URLs here
urlpatterns = [
    path("myfunctionbasedview/", views.myfunctionbasedview, name="myfunctionbasedview"),
]

# Add class based view URLs here
router = routers.SimpleRouter()
router.register("mymodelviewset", views.MyModelViewSet, basename="mymodelviewset")
urlpatterns += router.urls
