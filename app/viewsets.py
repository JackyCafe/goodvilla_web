'''
2023/8/24
googvilla01
viewsets.py
by yhlin
'''
import json
import logging

from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from app.models import DetailItem, MajorItem, SubItem, WorkRecord
from app.serializers import (DetailItemSerializer, MajorItemSerializer,
                             SubItemSerializer, WorkRecordSerializer)


class MajorItemViewSet(viewsets.ModelViewSet):
    queryset = MajorItem.objects.all()
    serializer_class = MajorItemSerializer

'''
首頁摘要
'''
class WorkRecordSummaryView(viewsets.ModelViewSet):
    queryset = WorkRecord.objects.all()
    serializer_class = WorkRecordSerializer

    @action(detail=True, methods=['get'])
    def summary(self, request,user_id, working_date):
        w_date = self.kwargs['working_date']
        user_id= self.kwargs['user_id']
        # def get_queryset(self):
    #     working_date = self.kwargs['working_date']
        try:
            date = datetime.strptime(working_date, '%Y-%m-%d').date()
            # working_month = datetime.strptime(working_date, '%Y-%m')
            logging.info(date)
            major_ids = (WorkRecord.objects
                         .filter(
                working_date=working_date
            ).values_list('detail__sub_item__major__id', flat=True).distinct())
            summary_data = []
            for major_id in major_ids:
                work_records = WorkRecord.objects.filter(
                    detail__sub_item__major__id=major_id,
                    working_date=working_date
                ).filter(user=user_id)

                daily_spend = work_records.aggregate(total_spend=models.Sum('spend_time'))
                daily_bonus = work_records.aggregate(total_bonus=models.Sum('bonus'))
                daily_moods = work_records.aggregate(total_moods=models.Sum('mood'))
                major_item = MajorItem.objects.get(pk=major_id)
                item = json.loads(f'"{major_item.item}"')

                summary_data.append({
                    'major_id': major_id,
                    'item':item,
                    'daily_spend': daily_spend['total_spend'] if daily_spend['total_spend'] is not None else 0,
                    'daily_bonus': daily_bonus['total_bonus'] if daily_bonus['total_bonus'] is not None else 0,
                    'daily_moods': daily_moods['total_moods'] if daily_moods['total_moods'] is not None else 0,

                })
            logging.info(summary_data)
            #
            return JsonResponse(summary_data, safe=False, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii': False})

        except ValueError:
            return Response(
                {"detail": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

'''每月摘要'''
class MonthBonusViewSet(viewsets.ModelViewSet):
    queryset = WorkRecord.objects.all()
    serializer_class = WorkRecordSerializer

    @action(methods=['get'], detail=True)
    def summary(self, request,year, month):
        try:
            year = int(year)
            month = int(month)

            monthly_bonus_by_major = WorkRecord.objects.filter(
                working_date__year=year,
                working_date__month=month
            ).annotate(
                total_bonus=Sum('bonus'),total_mins=Sum('spend_time')
            ).values('user__username', 'detail__sub_item__major__item', 'total_bonus', 'total_mins')

            result = {}
            for entry in monthly_bonus_by_major:
                username = entry['user__username']
                major = entry['detail__sub_item__major__item']
                total_bonus = entry['total_bonus']
                total_mins = entry['total_mins']
                if username not in result:
                    result[username] = []

                result[username].append({'major': major, 'bonus': total_bonus, 'total_mins': total_mins})

            return Response(result, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid year or month format'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # try:
        #     monthly_bonus_by_major = WorkRecord.objects.annotate(
        #         month=TruncMonth('working_date')
        #     ).values('month', 'user__username', 'detail__sub_item__major__item').annotate(
        #         total_bonus=Sum('bonus')
        #     )
        #
        #     result = []
        #     user_data = {}
        #
        #     for entry in monthly_bonus_by_major:
        #         month = entry['month'].strftime('%Y-%m')
        #         username = entry['user__username']
        #         major = entry['detail__sub_item__major__item']
        #         total_bonus = entry['total_bonus']
        #
        #         if username not in user_data:
        #             user_data[username] = []
        #
        #         user_data[username].append({'major': major, 'bonus': total_bonus})
        #
        #     for user, data in user_data.items():
        #         result.append({user: data})
        #
        #     return Response(result, status=status.HTTP_200_OK)
        #
        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubItemViewSet(viewsets.ModelViewSet):
    # queryset =  SubItem.objects.all()
    serializer_class = SubItemSerializer
    def get_queryset(self):
        major_id = self.kwargs['major_id']
        return SubItem.objects.filter(major_id=major_id)




class DetailItemViewSet(viewsets.ModelViewSet):
    # queryset = DetailItem.objects.all()
    serializer_class = DetailItemSerializer

    def get_queryset(self):
        sub_item_id = self.kwargs['subitem_id']
        return DetailItem.objects.filter(sub_item_id=sub_item_id)


class WorkRecordViewSet(viewsets.ModelViewSet):
    serializer_class = WorkRecordSerializer

    def get_queryset(self):
        detail_id = self.kwargs['detail_id']
        return WorkRecord.objects.filter(detail_id=detail_id)

class WorkRecordByDateViewSet(viewsets.ModelViewSet):
    serializer_class = WorkRecordSerializer

    def get_queryset(self):
        working_date = self.kwargs['working_date']
        # user_id = self.kwargs['user_id']

        return WorkRecord.objects.filter(working_date=working_date)

