from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, UsersAreaInfo
from .forms import ProfileForm, UserAreaForm
from django.db import IntegrityError
from .tables import ProfileTable
from django.http import HttpResponse
import numpy as np


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

            try:
                check_if_exists = Profile.objects.get(user_id=request.user)
            except Profile.DoesNotExist:
                return redirect('user_info')

            if check_if_exists:
                return redirect('user_home')
            else:
                return redirect('user_info')


@login_required
def user_info(request):
    if request.method == 'GET':
        form = ProfileForm

        context = {
            'form': form,
        }

        if request.user.is_staff and request.user.is_superuser:
            return redirect('user_dashboard')
        else:
            return render(request, 'test_app/dataentry.html', context)
    else:
        try:
            form = ProfileForm(request.POST)

            if form.is_valid():
                data = form.save(commit=False)
                data.user_id = request.user
                data.save()
            else:
                raise ValueError

            messages.success(request, 'Data entry saved successfully.')
            return redirect('user_home')
        except ValueError:
            messages.error(request, 'The system encountered an error. Please try again.')
            return redirect('user_info')


@login_required
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


@login_required
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


@login_required
def add_entry(request):
    if request.method == 'GET':
        form = UserAreaForm()

        context = {
            'form': form
        }

        return render(request, 'test_app/addentry.html', context)
    else:
        try:
            entry_form = UserAreaForm(request.POST, request.FILES)
            profile_id = Profile.objects.get(user_id=request.user)

            if entry_form.is_valid():
                save_entry = entry_form.save(commit=False)
                save_entry.profile_id = profile_id
                save_entry.save()
            else:
                raise ValueError

            messages.success(request, 'Entry saved successfully')
            return redirect('user_home')
        except ValueError:
            messages.error(request, 'Data entry encountered an error. Please try again.')
            return redirect('add_entry')


@login_required
def view_area(request, pk):
    if request.method == 'GET':
        profile_id = Profile.objects.get(user_id=request.user)
        user_area = get_object_or_404(UsersAreaInfo, id=pk, profile_id=profile_id)
        form = UserAreaForm(instance=user_area)

        context = {
            'user_area': user_area,
            'form': form
        }

        return render(request, 'test_app/viewarea.html', context)
    else:
        try:
            profile_id = Profile.objects.get(user_id=request.user)
            user_area = get_object_or_404(UsersAreaInfo, id=pk, profile_id=profile_id)
            entry_form = UserAreaForm(request.POST, request.FILES, instance=user_area)

            if entry_form.is_valid():
                save_entry = entry_form.save(commit=False)
                save_entry.profile_id = profile_id
                save_entry.save()
            else:
                raise ValueError

            messages.success(request, 'Update saved successfully')
            return redirect('view_area', user_area.id)
        except ValueError:
            messages.error(request, 'Update entry encountered an error. Please try again.')
            return redirect('view_area', user_area.id)


@login_required
def user_dashboard(request):
    if request.method == 'GET':
        if request.user.is_superuser is not True:
            return redirect('user_info')
        else:
            data_entries = Profile.objects.all()
            # entries = ProfileTable()

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
            }

            return render(request, 'test_app/dashboard.html', context)
    else:
        pass


@login_required
def view_user(request, pk):
    if request.method == 'GET':
        profile_info = get_object_or_404(Profile, id=pk)
        user_areas = UsersAreaInfo.objects.filter(profile_id=pk)

        context = {
            'user_areas': user_areas,
            'profile': profile_info,
        }

        return render(request, 'test_app/viewuser.html', context)
    else:
        pass


@login_required
def view_area_admin(request, pk):
    if request.method == 'GET':
        user_area = get_object_or_404(UsersAreaInfo, id=pk)

        context = {
            'user_area': user_area
        }

        return render(request, 'test_app/viewarea.html', context)
    else:
        pass
