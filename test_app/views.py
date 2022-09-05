from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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
        user = Profile.objects.get(user_id=request.user)
        user_areas = UsersAreaInfo.objects.filter(profile_id=user)

        context = {
            'user_areas': user_areas,
        }

        return render(request, 'test_app/user_home.html', context)
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
        pass


@login_required
def user_dashboard(request):
    if request.method == 'GET':
        if request.user.is_superuser is not True:
            return redirect('user_info')
        else:
            data_entries = Profile.objects.all()
            entries = ProfileTable()

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
                'entries': entries,
                'income': mean_income,
            }

            return render(request, 'test_app/dashboard.html', context)
    else:
        pass
