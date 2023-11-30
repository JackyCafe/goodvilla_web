from django.db import models

# Create your models here.
import  datetime
import logging

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

Mood_Choice = (('2', 2), ('1', 1), ('-1', -1), ('-2', -2))


# Create your models here.
# 大分類
class MajorItem(models.Model):
    item = models.CharField(max_length=8,blank=False)

    def __str__(self):
        return self.item


class SubItem(models.Model):
    major = models.ForeignKey(MajorItem,on_delete=models.CASCADE, related_name='major_id')
    sub_items = models.CharField(max_length=20,null=False)

    def __str__(self):
        return self.sub_items


class DetailItem(models.Model):
    sub_item = models.ForeignKey(SubItem,on_delete=models.CASCADE,related_name='subitem_id')
    detail = models.CharField(max_length=40,null=False)
    comment = models.CharField(max_length=40,null=True,blank=True,default='')

    def __str__(self):
        return self.detail



class WorkRecord(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    detail = models.ForeignKey(DetailItem,on_delete=models.CASCADE,name='detail')
    working_date = models.DateField(default=timezone.now(),verbose_name='工作日期')
    start_time = models.TextField(verbose_name='起始時間')
    end_time = models.TextField(verbose_name='結束時間')
    spend_time= models.IntegerField(default=0,verbose_name='花費時間')
    bonus = models.IntegerField(default=0,verbose_name='收費')
    mood = models.CharField(max_length=3,choices=Mood_Choice,default=0,verbose_name='能量指標')
    comment = models.TextField(max_length=200,null=True,blank=True)


    def calculate_spend_time(self):
        if self.start_time and self.end_time:
            time1=  datetime.datetime.strptime(self.end_time.strftime("%Y/%m/%d %H:%M:%S.%f"), "%Y/%m/%d %H:%M:%S.%f")
            time2=  datetime.datetime.strptime(self.start_time.strftime("%Y/%m/%d %H:%M:%S.%f"), "%Y/%m/%d %H:%M:%S.%f")
            time_diff = time1-time2
            self.spend_time = time_diff.total_seconds()/3600; #hours
            logging.info(f'time diff{time_diff}')
        self.save()

    def __str__(self):
        return '%s: %s'%(self.user, self.detail)