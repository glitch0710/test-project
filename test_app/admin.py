from django.contrib import admin
from .models import Profile, UsersAreaInfo, RegionCode, ProvincialCode, MunCityCode, BrgyCode


admin.site.register(Profile)
admin.site.register(UsersAreaInfo)
admin.site.register(RegionCode)
admin.site.register(ProvincialCode)
admin.site.register(MunCityCode)
admin.site.register(BrgyCode)
