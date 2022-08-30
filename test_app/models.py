from django.db import models


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
    address = models.TextField()
    income_annual = models.FloatField()

    def __str__(self):
        return self.first_name


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

    def __str__(self):
        return self.profile_id
