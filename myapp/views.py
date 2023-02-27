from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import MyModel
from .serializers import MyModelSerializer


@extend_schema(
    summary="MyModelViewSet",
    description="MyModelViewSet",
    responses=MyModelSerializer,
)
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer


@extend_schema(
    description="Return an HTTP response containing a histogram of berry growth times.",
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.STR,
            description="An image/png response containing the histogram plot.",
        ),
        500: OpenApiResponse(
            response=OpenApiTypes.OBJECT,
            description="A JSON response containing an error message and error code.",
        ),
    },
)
@api_view(["GET"])
def myfunctionbasedview(request: Request):
    return Response({"message": "Hello World!"})
