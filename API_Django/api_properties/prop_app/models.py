from django.db import models


class HousingType(models.Model):
    typeid = models.AutoField(db_column='TypeID', primary_key=True)
    typename = models.TextField(db_column='TypeName', unique=True)

    class Meta:
        managed = False
        db_table = 'HousingTypes'

    def __str__(self):
        return self.typename


class Property(models.Model):
    propertyid = models.AutoField(db_column='PropertyID', primary_key=True)
    typeid = models.ForeignKey('HousingType', models.DO_NOTHING, db_column='TypeID', blank=True, null=True)
    streetaddress = models.TextField(db_column='StreetAddress', unique=True)
    postalcode = models.IntegerField(db_column='PostalCode', blank=True, null=True)
    squaremeters = models.IntegerField(db_column='SquareMeters')
    monthlyrent = models.IntegerField(db_column='MonthlyRent')
    dailyrent = models.IntegerField(db_column='DailyRent')
    hasrenovation = models.BooleanField(db_column='HasRenovation', blank=True, null=True)
    metroproximity = models.FloatField(db_column='MetroProximity', blank=True, null=True)
    buildingfloors = models.IntegerField(db_column='BuildingFloors', blank=True, null=True)
    hasbalcony = models.BooleanField(db_column='HasBalcony', blank=True, null=True)
    hasparking = models.BooleanField(db_column='HasParking', blank=True, null=True)
    description = models.TextField(db_column='Description', blank=True, null=True)
    pets = models.BooleanField(db_column='Pets', blank=True, null=True)
    contactinfo = models.TextField(db_column='ContactInfo', blank=True, null=True)

    class Meta: 
        managed = False
        db_table = 'Properties'

    def __str__(self):
        return self.streetaddress
    

class Image(models.Model):
    imageid = models.AutoField(db_column='ImageID', primary_key=True)
    propertyid = models.ForeignKey('Property', models.DO_NOTHING, db_column='PropertyID', blank=True, null=True)
    imageurl = models.TextField(db_column='ImageURL', unique=True)

    class Meta:
        managed = False
        db_table = 'Images'

    def __str__(self):
        return self.imageurl