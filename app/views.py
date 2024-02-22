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
    '''註冊'''
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


# Todo
def report(request, year, month):
    '''月報表
       對應到http://127.0.0.1:8000/app/report/2024/02
    '''
    user = request.user
    permission = user.is_superuser
    year = int(year)
    month = int(month)

    try:
        '''如果是管理者看所有人資料'''
        if permission:
            datas = WorkRecord.objects.filter(
                working_date__year=year,
                working_date__month=month
            ).annotate(
                total_bonus=Sum('bonus'),
                total_time=Sum('spend_time'),
            ).values('user__username', 'detail__sub_item__major__item', 'total_bonus', 'total_time')
            result = {}

        else:
            '''非管理者看個人資料'''
            datas = WorkRecord.objects.filter(
                user_id=user,
                working_date__year=year,
                working_date__month=month
            ).annotate(
                total_bonus=Sum('bonus'),
                total_time=Sum('spend_time'),
            ).values('user__username', 'detail__sub_item__major__item', 'total_bonus', 'total_time')
            result = {}
        '''進行加總'''


        for entry in datas:
            username = entry['user__username']
            major = entry['detail__sub_item__major__item']
            total_bonus = entry['total_bonus']
            total_time = entry['total_time']
            #user 不在result 清單中，就加進去
            if username not in result:
                result[username] = []

            existing_entry = next((item for item in result[username] if item['major'] == major), None)
            if existing_entry:
                # If the major already exists, update the bonus
                existing_entry['bonus'] += total_bonus
                existing_entry['total_time'] += total_time
            else:
                # If the major doesn't exist, add a new entry
                result[username].append({'major': major, 'bonus': total_bonus, 'total_time': total_time})

        data={}
        for name,records in result.items():
            subtotal_bonus = sum(record['bonus'] for record in records)
            subtotal_total_time = sum(record['total_time'] for record in records)
            data[name] = {'major': '小計', 'bonus': subtotal_bonus, 'total_time': subtotal_total_time}

            result[name].append({'bonus': subtotal_bonus, 'total_time': subtotal_total_time})
        print(result)
        return render(request, 'account/report.html'
                      , {'results': result, 'data': data})
    except ValueError:
        return Response({'error': 'Invalid year or month format'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return HttpResponse({str(e)})
