"""
URL configuration for api_properties project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from prop_app.views import HousingTypeViewSet, PropertyViewSet, ImageViewSet, PropertyFilterView
from rest_framework.routers import DefaultRouter

router_housingtype, router_properties, router_images = DefaultRouter(
), DefaultRouter(), DefaultRouter()
router_housingtype.register(r'housingtype', HousingTypeViewSet)
router_properties.register(r'properties', PropertyViewSet)
router_images.register(r'images', ImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all/', include(router_housingtype.urls)),
    path('all/', include(router_properties.urls)),
    path('all/', include(router_images.urls)),
    path('api/properties/', PropertyFilterView.as_view(), name='property-filter')
]
