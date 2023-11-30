from django.shortcuts import render

# Create your views here.
import sys

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

# Create your views here.
import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.forms import WorkRecordForm
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
    return  render(request,'app/index.html',{'major':major})


def subitem_view(request,id):
    item = get_list_or_404(SubItem,major_id=id)
    return  render(request,'app/sub_views.html',{'subitems':item})


def detail_view(request,id):
    item = get_list_or_404(DetailItem,sub_item_id=id)
    return  render(request,'app/detail_views.html',{'detailitems':item})

#
def create_work_record(request,id):
    user_id = request.session.get('user')
    #yhlin
    user = User.objects.get(id=user_id)
    detail = get_object_or_404(DetailItem,id = id)
    # logging.info(detail)
    intaial_data={'user':user,
                  'detail':detail}
    logging.info(request.POST)
    if request.method == 'POST':
        form = WorkRecordForm(request.POST or None,initial=intaial_data)
        if form.is_valid():
            instance = form.save(commit=False)  # The overridden save() method will call calculate_spend_time() before saving
            return redirect('app:index')  # Replace 'success_url' with the URL to redirect after form submission
    else:
       # form = WorkRecordForm()
        form = WorkRecordForm(initial=intaial_data)
    return render(request, 'app/create_work_record_views.html', {'form': form})


