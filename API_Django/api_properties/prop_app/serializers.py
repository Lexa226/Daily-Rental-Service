from .models import HousingType, Property, Image
from rest_framework import serializers


class HousingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingType
        fields = ('typename',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('imageurl',) 

class PropertySerializer(serializers.ModelSerializer):
    typename = serializers.CharField(source='typeid.typename', read_only=True)
    images = serializers.SerializerMethodField() 

    class Meta:
        model = Property
        fields = ['propertyid', 'typename', 'streetaddress', 'postalcode', 'squaremeters', 'monthlyrent', 'dailyrent', 
                  'hasrenovation', 'metroproximity', 'buildingfloors', 'hasbalcony', 'hasparking', 'description',
                  'pets', 'contactinfo', 'images']

    def get_images(self, obj):
        images = Image.objects.filter(propertyid=obj)
        return [img.imageurl for img in images] 