import json
from typing import Type

from django.contrib.auth import authenticate, login
from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

# Create your views here.
import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.forms import WorkRecordForm, UserRegistrationForm
from app.models import MajorItem, SubItem, DetailItem, WorkRecord
from app.serializers import WorkRecordSerializer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s ',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.FileHandler("mylog.log"),
                        logging.StreamHandler(sys.stdout)
                    ]
                    )


@login_required
def index(request):
    request.session['user'] = request.user.id
    major = MajorItem.objects.all()
    return render(request, 'app/index.html', {'major': major})


def subitem_view(request, id):
    item = get_list_or_404(SubItem, major_id=id)
    return render(request, 'app/sub_views.html', {'subitems': item})


def detail_view(request, id):
    item = get_list_or_404(DetailItem, sub_item_id=id)
    return render(request, 'app/detail_views.html', {'detailitems': item})


#

def create_work_record(request, id):
    user_id = request.session.get('user')
    # yhlin
    user = User.objects.get(id=user_id)
    detail = get_object_or_404(DetailItem, id=id)
    # logging.info(detail)
    intaial_data = {'user': user,
                    'detail': detail}
    logging.info(request.POST)
    if request.method == 'POST':
        form = WorkRecordForm(request.POST or None, initial=intaial_data)
        if form.is_valid():
            instance = form.save(
                commit=False)  # The overridden save() method will call calculate_spend_time() before saving
            return redirect('app:index')  # Replace 'success_url' with the URL to redirect after form submission
    else:
        # form = WorkRecordForm()
        form = WorkRecordForm(initial=intaial_data)
    return render(request, 'app/create_work_record_views.html', {'form': form})


@login_required
def dashboard(request):
    request.session['user'] = request.user.id
    return redirect('app:index')


def register(request):
    """
    註冊

    """
    user_form: UserRegistrationForm
    new_user: User
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('app:dashboard')

        else:
            return HttpResponse(user_form.errors)
    else:
        user_form = UserRegistrationForm
    return render(request, 'account/register.html', {'user_form': user_form})


# todo 個人月報
def person_report(request, year, month):
    """
    對應到http://127.0.0.1:8000/app/report/2024/02

    :param request:
    :param year:
    :param month:
    :return:
    """
    user = request.user  # 抓登入user
    permission = user.is_superuser
    year = int(year)
    month = int(month)
    result = {}
    try:
        # 如果是superuser
        if permission:
            datas = WorkRecord.objects.filter(
                working_date__year=year,
                working_date__month=month
            ).annotate(
                total_bonus=Sum('bonus'),
                total_time=Sum('spend_time'),
            ).values('user__username', 'detail__sub_item__major__item', 'total_bonus', 'total_time')

        else:
            # 一般user
            datas = WorkRecord.objects.filter(
                working_date__year=year,
                working_date__month=month,
                user_id=user
            ).annotate(
                total_bonus=Sum('bonus'),
                total_time=Sum('spend_time'),
            ).values('user__username', 'detail__sub_item__major__item', 'total_bonus', 'total_time')
        logging.info(datas)
        for entry in datas:
            username = entry['user__username']
            major = entry['detail__sub_item__major__item']
            total_bonus = entry['total_bonus']
            total_time = entry['total_time']
            # reset result
            if username not in result:
                result[username] = []
            exist_entry = next((item for item in result[username] if item['major'] == major), None)

            if exist_entry:
                exist_entry['total_bonus'] += total_bonus
                exist_entry['total_time'] += total_time
            else:
                result[username].append({'major': major, 'total_bonus': total_bonus, 'total_time': total_time})
        return render(request, 'account/person_report.html'
                      , {'results': result})
    except ValueError:
        return Response({'error': 'Invalid year or month format'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return HttpResponse(str(e))


# Todo
def report(request, year, month):
    """
    月報表
    對應到http://127.0.0.1:8000/app/report/2024/02

    :param request:
    :param year:
    :param month:
    :return:
    """

    user = request.user
    permission = user.is_superuser
    year = int(year)
    month = int(month)

    try:

        if permission:
            """
                    如果是管理者看所有人資料
                    摘要 食,衣,住...等摘要資料
                     主項   bouns total_spend 
                     食      0     14280
                    """

            datas = (WorkRecord.objects.filter(
                working_date__year=year,
                working_date__month=month
            ).values('detail__sub_item__major__item')
            .annotate(
                total_bonus=Sum('bonus'),
                total_time=Sum('spend_time')
            ))

            """ 
                摘要 食...衣 ...住..行 by 個人
                user   摘要  bonus total_spend
                yhlin  食    0      1220
                yhlin  住    0      1330
            
            """
            user_datas = WorkRecord.objects.filter(
                working_date__year=year,
                working_date__month=month
            ).values('user__username', 'detail__sub_item__major__item').annotate(
                total_bonus=Sum('bonus'),
                total_time=Sum('spend_time')
            ).order_by()
            logging.info(user_datas)
            return render(request, 'account/report.html',
                          {'datas': datas, 'user_datas': user_datas})
        else:
            return HttpResponse("權限不足")
    except ValueError:
        return Response({'error': 'Invalid year or month format'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return HttpResponse(f'error:{str(e)}')
