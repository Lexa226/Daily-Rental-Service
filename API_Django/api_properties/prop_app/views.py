from .models import HousingType, Property, Image
from .serializers import HousingTypeSerializer, PropertySerializer, ImageSerializer
from rest_framework import viewsets
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .pagination import StandardResultsSetPagination
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ParseError


class HousingTypeViewSet(viewsets.ModelViewSet):
    queryset = HousingType.objects.all()
    serializer_class = HousingTypeSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


@method_decorator(csrf_exempt, name='dispatch')
class PropertyFilterView(APIView, StandardResultsSetPagination):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params.dict()
        page_keys = ['page', 'limit']
        filter_args = {}
        city_filter = None

        for key, value in query_params.items():
            if key not in page_keys:
                value = value.lower()
                if value in ["true", "false"]:
                    value = value == 'true'
                elif key == "typename":
                    key = "typeid__typename"

                if key == "city":
                    # Используйте .capitalize() если город записан с заглавной буквы
                    city_filter = value.capitalize()
                else:
                    filter_args[key] = value

        try:
            properties = Property.objects.filter(**filter_args)
            if city_filter:
                # Фильтрация с учетом регистра и точного совпадения города
                properties = properties.filter(
                    streetaddress__istartswith=f"{city_filter} ")

            page = self.paginate_queryset(properties, request, view=self)
            if page is not None:
                serializer = PropertySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'An unexpected error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
