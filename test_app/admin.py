from django.contrib import admin
from .models import Profile, UsersAreaInfo, RegionCode, ProvincialCode, \
    MunCityCode, BrgyCode, ProfileAttachments, Farmer, FarmerDependents, AreaCrop


admin.site.register(Profile)
admin.site.register(UsersAreaInfo)
admin.site.register(RegionCode)
admin.site.register(ProvincialCode)
admin.site.register(MunCityCode)
admin.site.register(BrgyCode)
admin.site.register(ProfileAttachments)
admin.site.register(Farmer)
admin.site.register(FarmerDependents)
admin.site.register(AreaCrop)
