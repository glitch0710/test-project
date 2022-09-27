from django.db import models
from django.conf import settings

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


class Farmer(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    PERSON_GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    assigned_id = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    middle_name = models.CharField(max_length=200, blank=False)
    gender = models.CharField(max_length=1, choices=PERSON_GENDER, default=MALE)
    region = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    muncity = models.CharField(max_length=200)
    brgy = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    tin = models.CharField(max_length=20, blank=True, null=True)
    philhealth = models.CharField(max_length=20, blank=True, null=True)
    sss = models.CharField(max_length=20, blank=True, null=True)
    pagibig = models.CharField(max_length=20, blank=True, null=True)
    civil_status = models.CharField(max_length=20, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(default=None)
    spouse = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.first_name


class FarmerDependents(models.Model):
    farmer = models.ForeignKey(Farmer, models.CASCADE, db_column='farmer')
    dependent_name = models.CharField(max_length=250, blank=False)
    age = models.IntegerField()

    def __str__(self):
        return self.farmer


# Farmers
class ProfileAttachments(models.Model):
    farmer_id = models.ForeignKey(Farmer, models.CASCADE, db_column='farmer_id')
    id_picture = models.FileField(upload_to='profile_attachments/id/%Y%m%d')
    cedula = models.FileField(upload_to='profile_attachments/cedula/%Y%m%d')
    brgy_clearance = models.FileField(upload_to='profile_attachments/brgy_clearance/%Y%m%d')
    tax_dec = models.FileField(upload_to='profile_attachments/tax_dec/%Y%m%d')
    valid_id_one = models.FileField(upload_to='profile_attachments/valid_id/%Y%m%d')
    valid_id_two = models.FileField(upload_to='profile_attachments/valid_id/%Y%m%d')


class UsersAreaInfo(models.Model):
    RICE = 'Rice'
    CORN = 'Corn'
    SUGARCANE = 'Sugarcane'

    PLANTED = [
        (RICE, 'Rice'),
        (CORN, 'Corn'),
        (SUGARCANE, 'Sugarcane'),
    ]

    farmer_id = models.ForeignKey(Farmer, models.CASCADE, db_column='farmer_id')
    total_area = models.FloatField()
    crop_planted = models.CharField(max_length=9, choices=PLANTED, default=RICE)
    remarks = models.CharField(max_length=100)
    sketch_plan = models.FileField(upload_to='documents_sp/', max_length=254, blank=True)
    map = models.FileField(upload_to='documents_map/', max_length=254, blank=True)
    google_earth = models.FileField(upload_to='documents_ge/', max_length=254, blank=True)
    area_coordinates = models.FileField(upload_to='documents_coordinates/', max_length=254, blank=True)
    profile_field = models.CharField(max_length=250)
    soil_ph = models.IntegerField()
    region = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    muncity = models.CharField(max_length=200)
    brgy = models.CharField(max_length=200)


class AreaCrop(models.Model):
    RICE = 'Rice'
    CORN = 'Corn'
    SUGARCANE = 'Sugarcane'

    PLANTED = [
        (RICE, 'Rice'),
        (CORN, 'Corn'),
        (SUGARCANE, 'Sugarcane'),
    ]

    crop_planted = models.CharField(max_length=9, choices=PLANTED, default=RICE)
    status = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)


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

