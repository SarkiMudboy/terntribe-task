from rest_framework.exceptions import status
from rest_framework.request import HttpRequest

from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from .exceptions import ResourceNotFoundException
from rest_framework.permissions import AllowAny
from .serializers import CauseSerializer, ContributionSerializer
from .models import Cause
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(tags=["Cause List, and Create New Cause"])
class CauseView(viewsets.ModelViewSet):

    queryset = Cause.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CauseSerializer
    lookup_field = "id"

    def get_object(self) -> Cause:
        try:
            return self.get_queryset().get(
                id=self.kwargs.get(self.lookup_field)
            )
        except Cause.DoesNotExist:
            raise ResourceNotFoundException("Cause Not Found")

    @extend_schema(
        summary="Add Cause",
        description="This POST method adds a new cause",
        request=CauseSerializer,
        responses={
            201: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def create(self, request: HttpRequest, **kwargs) -> HttpResponse:

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            _ = serializer.save()

            return JsonResponse(
                {
                    "message": "Cause created",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED,
                },
                status=status.HTTP_201_CREATED,
            )

        return JsonResponse(
            {
                "message": "Cause create failed",
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="List Cause",
        description="This GET method lists all causes",
        responses={
            201: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def list(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        cause = self.get_queryset()
        serializer = self.serializer_class(cause, many=True)
        return JsonResponse(
            {
                "message": "Retrieve Causes Success",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve Cause",
        description="This GET method gets an existing cause specified by id",
        responses={
            201: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def retrieve(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:

        cause = self.get_object()
        serializer = self.serializer_class(cause)
        return JsonResponse(
            {
                "message": "Retrieve Cause Success",
                "data": serializer.data,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update Cause",
        description="This PUT method updates an existing cause provided by id",
        request=CauseSerializer,
        responses={
            201: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def update(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        cause = self.get_object()
        serializer = self.serializer_class(cause, data=request.data)

        if serializer.is_valid():
            _ = serializer.save()

            return JsonResponse(
                {
                    "message": "Cause updated",
                    "data": serializer.data,
                    "status": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )

        return JsonResponse(
            {
                "message": "Cause update failed",
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Delete Cause",
        description="This DELETE method deletes a cause specified by id",
        responses={
            201: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    def delete(self, request: HttpRequest, *args, **kwargs):
        cause = self.get_object()
        cause.delete()
        return JsonResponse(
            {
                "message": "Cause delete success",
                "status": status.HTTP_204_NO_CONTENT,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        summary="Add Contribution",
        description="This POST method adds a new contribution",
        request=ContributionSerializer,
        responses={
            201: OpenApiResponse(description="Json Response"),
            400: OpenApiResponse(description="Validation error"),
        },
    )
    @action(methods=["POST"], detail=True, url_path="contribute")
    def contribute(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:

        cause = self.get_object()
        serializer = ContributionSerializer(data=request.data)
        if serializer.is_valid():
            _ = serializer.save(cause)

            return JsonResponse(
                {
                    "message": "Contibution created",
                    "data": serializer.data,
                    "status": status.HTTP_201_CREATED,
                },
                status=status.HTTP_201_CREATED,
            )

        return JsonResponse(
            {
                "message": "Contibution create failed",
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
