from django.db import models
from django.conf import settings

# Farmers
class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    PERSON_GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=PERSON_GENDER, default=MALE)
    region = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    muncity = models.CharField(max_length=200)
    brgy = models.CharField(max_length=200)
    address = models.TextField()
    income_annual = models.FloatField(default=0, blank=True, null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

# Farmers
class ProfileAttachments(models.Model):
    profile_id = models.ForeignKey(Profile, models.CASCADE, db_column='profile_id')
    id_picture = models.FileField(upload_to='profile_attachments/id/%Y%m%d')
    cedula = models.FileField(upload_to='profile_attachments/cedula/%Y%m%d')
    brgy_clearance = models.FileField(upload_to='profile_attachments/brgy_clearance/%Y%m%d')
    tax_dec = models.FileField(upload_to='profile_attachments/tax_dec/%Y%m%d')
    valid_id_one = models.FileField(upload_to='profile_attachments/valid_id/%Y%m%d')
    valid_id_two = models.FileField(upload_to='profile_attachments/valid_id/%Y%m%d')

    def __str__(self):
        return self.profile_id


class UsersAreaInfo(models.Model):
    RICE = 'Rice'
    CORN = 'Corn'
    SUGARCANE = 'Sugarcane'

    PLANTED = [
        (RICE, 'Rice'),
        (CORN, 'Corn'),
        (SUGARCANE, 'Sugarcane'),
    ]

    profile_id = models.ForeignKey(Profile, models.CASCADE, db_column='profile_id')
    total_area = models.FloatField()
    crop_planted = models.CharField(max_length=9, choices=PLANTED, default=RICE)
    remarks = models.CharField(max_length=100)
    sketch_plan = models.FileField(upload_to='documents_sp/', max_length=254)
    map = models.FileField(upload_to='documents_map/', max_length=254)
    google_earth = models.FileField(upload_to='documents_ge/', max_length=254)
    profile_field = models.CharField(max_length=250)
    soil_ph = models.IntegerField()
    region = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    muncity = models.CharField(max_length=200)
    brgy = models.CharField(max_length=200)


class RegionCode(models.Model):
    psgc_code = models.CharField(max_length=20)
    region_name = models.CharField(max_length=200)
    reg_code = models.IntegerField()

    def __str__(self):
        return self.region_name


class ProvincialCode(models.Model):
    prov_psgc_code = models.CharField(max_length=20)
    province_name = models.CharField(max_length=200)
    region_code = models.IntegerField()
    prov_code = models.IntegerField()

    def __str__(self):
        return self.province_name


class MunCityCode(models.Model):
    muncity_psgc_code = models.CharField(max_length=20)
    muncity_name = models.CharField(max_length=200)
    region_code = models.IntegerField()
    province_code = models.IntegerField()
    muncity_code = models.IntegerField()

    def __str__(self):
        return self.muncity_name


class BrgyCode(models.Model):
    brgy_psgc_code = models.CharField(max_length=20)
    brgy_name = models.CharField(max_length=200)
    region_code = models.IntegerField()
    province_code = models.IntegerField()
    muncity_code = models.IntegerField()

    def __str__(self):
        return self.brgy_name

