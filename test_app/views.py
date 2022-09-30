from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, UsersAreaInfo, RegionCode, ProvincialCode, MunCityCode, BrgyCode, Farmer, AreaCrop
from .forms import ProfileForm, UserAreaForm, FarmerForm, FarmerAttachmentsForm, \
    UserAreaEngineerForm, UserAreaTechnicalForm, AreaCropForm
from django.db import IntegrityError
from .tables import ProfileTable
from django.http import HttpResponse, JsonResponse
import numpy as np
import json


def login_user(request):
    if request.method == 'GET':
        return render(request, 'test_app/home.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Wrong username or password. Please try again.')
            return redirect('login_user')
        else:
            login(request, user)

            if request.user.is_staff and request.user.is_superuser:
                return redirect('user_dashboard')
            else:
                if user.groups.all()[0].id == 1:
                    return redirect('user_home')
                elif user.groups.all()[0].id == 2:
                    return redirect('user_engineer')

            # try:
            #     check_if_exists = Profile.objects.get(user_id=request.user)
            # except Profile.DoesNotExist:
            #     return redirect('user_info')
            #
            # if check_if_exists:
            #     return redirect('user_home')
            # else:
            #     return redirect('user_info')


@login_required(login_url='/')
def user_info(request):
    if request.method == 'GET':
        # form = ProfileForm()
        regions = RegionCode.objects.all()
        farmer_list = Farmer.objects.all()

        context = {
            'data_entries': farmer_list,
            'regions': regions,
        }

        if request.user.is_staff and request.user.is_superuser:
            return redirect('user_dashboard')
        else:
            return render(request, 'test_app/staffdashboard.html', context)
    else:
        try:
            form = ProfileForm(request.POST)

            if form.is_valid():
                data = form.save(commit=False)
                data.user_id = request.user
                data.region = request.POST['region']
                data.province = request.POST['province']
                data.muncity = request.POST['muncity']
                data.brgy = request.POST['brgy']
                data.income_annual = 0

                address = str(get_brgy(request.POST['brgy'])) + ', ' \
                          + str(get_muncity(request.POST['muncity'])) + ', ' \
                          + str(get_province(request.POST['province']))

                data.address = address
                data.save()
            else:
                raise ValueError

            messages.success(request, 'Data entry saved successfully.')
            return redirect('user_home')
        except ValueError:
            messages.error(request, 'The system encountered an error. Please try again.')
            return redirect('user_info')


@login_required(login_url='/')
def add_farmer(request):
    if request.method == 'GET':
        form = FarmerForm()
        form_attachments = FarmerAttachmentsForm()
        regions = RegionCode.objects.all()

        context = {
            'form': form,
            'form_attachments': form_attachments,
            'regions': regions,
        }
        return render(request, 'test_app/newfarmer.html', context)
    else:
        try:
            primary_form = FarmerForm(request.POST)
            attachment_form = FarmerAttachmentsForm(request.POST, request.FILES)

            if primary_form.is_valid() and attachment_form.is_valid():
                data = primary_form.save(commit=False)
                data.region = request.POST['region']
                data.province = request.POST['province']
                data.muncity = request.POST['muncity']
                data.brgy = request.POST['brgy']

                address = str(get_brgy(request.POST['brgy'])) + ', ' \
                          + str(get_muncity(request.POST['muncity'])) + ', ' \
                          + str(get_province(request.POST['province']))

                data.address = address
                data.save()

                attchmnts = attachment_form.save(commit=False)
                farmer = Farmer.objects.get(id=data.id)
                attchmnts.farmer_id = farmer
                attchmnts.save()

                messages.success(request, 'Farmer profile saved successfully.')
                return redirect('user_info')
            else:
                messages.error(request, 'Form did not validate, please fill-up the form properly.')
                return redirect('add_farmer')
        except ValueError:
            messages.error(request, 'Data entry encountered an error. Please try again.')
            return redirect('add_farmer')


@login_required(login_url='/')
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_user')


def register_user(request):
    if request.method == 'GET':
        return render(request, 'test_app/register.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('user_info')
            except IntegrityError:
                messages.error(request, 'That username has already been taken. Please try another one.')
                return redirect('register_user')


@login_required(login_url='/')
def user_home(request):
    if request.method == 'GET':
        try:
            user = Profile.objects.get(user_id=request.user)
            user_areas = UsersAreaInfo.objects.filter(profile_id=user)

            context = {
                'user_areas': user_areas,
            }

            return render(request, 'test_app/user_home.html', context)
        except Profile.DoesNotExist:
            # messages.error(request, 'No matching profile. Please accomplish this form first.')
            return redirect('user_info')
    else:
        pass


@login_required(login_url='/')
def add_entry(request):
    if request.method == 'GET':
        form = UserAreaTechnicalForm()
        regions = RegionCode.objects.all()

        context = {
            'form': form,
            'regions': regions
        }

        return render(request, 'test_app/addentry.html', context)
    else:
        try:
            entry_form = UserAreaTechnicalForm(request.POST, request.FILES)

            if entry_form.is_valid():
                save_entry = entry_form.save(commit=False)
                save_entry.region = int(request.POST.get('region'))
                save_entry.province = int(request.POST.get('province'))
                save_entry.muncity = int(request.POST.get('muncity'))
                save_entry.brgy = int(request.POST.get('brgy'))
                save_entry.save()
            else:
                raise ValueError

            form_crop = AreaCropForm()
            context = {
                'area_id': save_entry.id,
                'form_crop': form_crop,
            }

            return render(request, 'test_app/addcrop.html', context)
        except ValueError:
            messages.error(request, 'Data entry encountered an error. Please try again.')
            return redirect('add_entry')


@login_required(login_url='/')
def add_crop(request):
    if request.method == 'POST':
        try:
           
            form = AreaCropForm(request.POST)

            if form.is_valid():
                new_area = form.save(commit=False)

                area = request.POST['area']
                area_id = UsersAreaInfo.objects.get(id=area)
                new_area.area_id = area_id

                new_area.save()

                crops = list(AreaCrop.objects.filter(area_id=area_id).values())
                print(crops)
                context = {
                    'crops': crops
                }

                return JsonResponse(data=crops, safe=False)

        except ValueError:
            messages.error(request, 'Data entry encountered an error. Please try again.')
            return redirect('add_entry')
    # else:
    #     form = AreaCropForm()
    #
    #     context = {
    #         'form_crop': form
    #     }
    #
    #     return render(request, 'test_app/addcrop.html', context)


@login_required(login_url='/')
def view_area(request, pk):
    if request.method == 'GET':
        user_area = get_object_or_404(UsersAreaInfo, id=pk)
        form = UserAreaTechnicalForm(instance=user_area)
        user_group = request.user.groups.all()[0].id

        farm_location = str(get_brgy(user_area.brgy)) + ', ' \
                      + str(get_muncity(user_area.muncity)) + ', ' \
                      + str(get_province(user_area.province))

        context = {
            'user_area': user_area,
            'farm_location': farm_location,
            'form': form,
            'user_group': user_group,
        }

        return render(request, 'test_app/viewarea.html', context)
    else:
        try:
            user_area = get_object_or_404(UsersAreaInfo, id=pk)
            entry_form = UserAreaForm(request.POST, request.FILES, instance=user_area)

            if entry_form.is_valid():
                entry_form.save()
            else:
                raise ValueError

            messages.success(request, 'Update saved successfully')
            return redirect('view_area', user_area.id)
        except ValueError:
            messages.error(request, 'Update entry encountered an error. Please try again.')
            return redirect('view_area', user_area.id)


@login_required(login_url='/')
def user_dashboard(request):
    if request.method == 'GET':
        if request.user.is_superuser is not True:
            return redirect('user_info')
        else:
            data_entries = Farmer.objects.all()
            regions = RegionCode.objects.all()

            raw_income = Profile.objects.all()
            list_income = []

            if not raw_income:
                mean_income = 0
            else:
                list_income.clear()
                for every_income in raw_income:
                    list_income.append(every_income.income_annual)

                np_income = np.array([list_income])
                mean_income = np.mean(np_income)

            context = {
                'data_entries': data_entries,
                'income': mean_income,
                'regions': regions,
            }

            return render(request, 'test_app/dashboard.html', context)
    else:
        profile_datas = Farmer.objects.all()

        searched_data = request.POST.get('search')
        region = int(request.POST.get('region'))
        province = int(request.POST.get('province'))
        muncity = int(request.POST.get('muncity'))
        brgy = int(request.POST.get('brgy'))

        if searched_data != '' and searched_data is not None:
            profile_datas = profile_datas.filter(first_name__icontains=searched_data)

        if region != 0:
            profile_datas = profile_datas.filter(region=region)

        if province != 0:
            profile_datas = profile_datas.filter(province=province)

        if muncity != 0:
            profile_datas = profile_datas.filter(muncity=muncity)

        if brgy != 0:
            profile_datas = profile_datas.filter(brgy=brgy)

        regions = RegionCode.objects.all()

        context = {
            'data_entries': profile_datas,
            'regions': regions,
        }

        return render(request, 'test_app/dashboard.html', context)


@login_required(login_url='/')
def viewarea_dashboard(request):
    if request.method == 'GET':
        data_entries = UsersAreaInfo.objects.all()
        regions = RegionCode.objects.all()

        pa = data_entries
        list_pa = []

        if not pa:
            productive_area = 0
        else:
            list_pa.clear()
            for area in pa:
                list_pa.append(area.total_area)

            np_pa = np.array([list_pa])
            productive_area = np.sum(np_pa)

        context = {
            'data_entries': data_entries,
            'productive_area': productive_area,
            'regions': regions,
        }

        return render(request, 'test_app/viewarea_dashboard.html', context)
    else:
        profile_datas = UsersAreaInfo.objects.all()

        searched_data = request.POST.get('search')
        region = int(request.POST.get('region'))
        province = int(request.POST.get('province'))
        muncity = int(request.POST.get('muncity'))
        brgy = int(request.POST.get('brgy'))

        if searched_data != '' and searched_data is not None:
            profile_datas = profile_datas.filter(id__icontains=searched_data)

        if region != 0:
            profile_datas = profile_datas.filter(region=region)

        if province != 0:
            profile_datas = profile_datas.filter(province=province)

        if muncity != 0:
            profile_datas = profile_datas.filter(muncity=muncity)

        if brgy != 0:
            profile_datas = profile_datas.filter(brgy=brgy)

        regions = RegionCode.objects.all()

        pa = profile_datas
        list_pa = []

        if not pa:
            productive_area = 0
        else:
            list_pa.clear()
            for area in pa:
                list_pa.append(area.total_area)

            np_pa = np.array([list_pa])
            productive_area = np.sum(np_pa)

        context = {
            'data_entries': profile_datas,
            'productive_area': productive_area,
            'regions': regions,
        }

        return render(request, 'test_app/viewarea_dashboard.html', context)


@login_required(login_url='/')
def user_list(request):
    if request.method == 'GET':
        data_entries = Profile.objects.all()
        regions = RegionCode.objects.all()
        groups = Group.objects.all()
        form = ProfileForm()
        userform = UserCreationForm()

        context = {
            'data_entries': data_entries,
            'form': form,
            'regions': regions,
            'userform': userform,
            'groups': groups,
        }
        return render(request, 'test_app/users.html', context)
    else:
        try:
            data = ProfileForm(request.POST)

            if data.is_valid():
                if request.POST.get('password1') == request.POST.get('password2'):
                    user_credentials = User.objects.create_user(
                        username=request.POST.get('username'),
                        email=request.POST.get('email'),
                        password=request.POST.get('password1'),
                    )

                    user_credentials.save()
                else:
                    messages.error(request, 'Passwords did not match. Please try again.')
                    return redirect('user_list')

                new_user = data.save(commit=False)
                new_user.region = int(request.POST.get('region'))
                new_user.province = int(request.POST.get('province'))
                new_user.muncity = int(request.POST.get('muncity'))
                new_user.brgy = int(request.POST.get('brgy'))
                new_user.income_annual = 0
                new_user.user_id = request.user

                address = str(get_brgy(request.POST['brgy'])) + ', ' \
                          + str(get_muncity(request.POST['muncity'])) + ', ' \
                          + str(get_province(request.POST['province']))

                new_user.address = address

                new_user.save()

                user_group = Group.objects.get(id=request.POST['usergroup'])
                user_group.user_set.add(user_credentials)

                messages.success(request, 'New user saved successfully')
                return redirect('user_list')
            else:
                raise ValueError
        except ValueError:
            messages.error(request, "Error encountered upon saving new user. Please try again.")
            return redirect('user_list')
        except IntegrityError:
            messages.error(request, 'That username has already been taken. Please try another one.')
            return redirect('user_list')


@login_required(login_url='/')
def view_user(request, pk):
    if request.method == 'GET':
        profile_info = get_object_or_404(Farmer, id=pk)
        user_areas = UsersAreaInfo.objects.filter(farmer_id=pk)

        context = {
            'user_areas': user_areas,
            'profile': profile_info,
        }

        return render(request, 'test_app/viewuser.html', context)
    else:
        pass


@login_required(login_url='/')
def view_area_admin(request, pk):
    if request.method == 'GET':
        user_area = get_object_or_404(UsersAreaInfo, id=pk)

        farm_location = str(get_brgy(user_area.brgy)) + ', ' \
                        + str(get_muncity(user_area.muncity)) + ', ' \
                        + str(get_province(user_area.province))

        context = {
            'user_area': user_area,
            'farm_location': farm_location,
        }

        return render(request, 'test_app/viewarea.html', context)
    else:
        pass


@login_required(login_url='/')
def engineer_view_area(request, pk):
    if request.method == 'GET':
        user_area = get_object_or_404(UsersAreaInfo, id=pk)
        form = UserAreaEngineerForm(instance=user_area)

        farm_location = str(get_brgy(user_area.brgy)) + ', ' \
                        + str(get_muncity(user_area.muncity)) + ', ' \
                        + str(get_province(user_area.province))

        context = {
            'user_area': user_area,
            'farm_location': farm_location,
            'form': form,
        }

        return render(request, 'test_app/engineerviewarea.html', context)
    else:
        try:
            user_area = get_object_or_404(UsersAreaInfo, id=pk)
            engr_update = UserAreaEngineerForm(request.POST, request.FILES, instance=user_area)

            if engr_update.is_valid():
                engr_update.save()

                messages.success(request, 'Update saved successfully.')
                return redirect('engineer_view_area', pk)
            else:
                messages.error(request, 'Record updating encountered an error. Please try again.')
                return redirect('engineer_view_area', pk)
        except ValueError:
            messages.error(request, 'Record updating encountered an error. Please try again.')
            return redirect('engineer_view_area', pk)


@login_required(login_url='/')
def user_engineer(request):
    if request.method == 'GET':
        user_areas = UsersAreaInfo.objects.all()

        context = {
            'user_areas': user_areas,
        }
        return render(request, 'test_app/engineer.html', context)
    else:
        pass


@login_required(login_url='/')
def province_filtered(request, pk):
    provinces = ProvincialCode.objects.filter(region_code=pk)
    return JsonResponse({"provinces":list(provinces.values())})


@login_required(login_url='/')
def muncity_filtered(request, pk):
    muncities = MunCityCode.objects.filter(province_code=pk)
    return JsonResponse({"muncities": list(muncities.values())})


@login_required(login_url='/')
def brgy_filtered(request, pk):
    brgys = BrgyCode.objects.filter(muncity_code=pk)
    return JsonResponse({"brgys": list(brgys.values())})


def get_region(region_id):
    if region_id != 0:
        region_name = RegionCode.objects.filter(reg_code=region_id).region_name
        return region_name


def get_province(province_id):
    if province_id != 0:
        province_name = ProvincialCode.objects.get(prov_code=province_id).province_name
        return province_name


def get_muncity(muncity_id):
    if muncity_id != 0:
        muncity_name = MunCityCode.objects.get(muncity_code=muncity_id).muncity_name
        return muncity_name


def get_brgy(brgy_id):
    if brgy_id != 0:
        brgy_name = BrgyCode.objects.get(brgy_psgc_code=brgy_id).brgy_name
        return brgy_name