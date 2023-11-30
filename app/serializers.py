'''
2023/8/24
googvilla01
serializers.py
by yhlin
'''
from rest_framework import serializers

from app.models import MajorItem, SubItem,DetailItem,WorkRecord


class MajorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorItem
        fields = '__all__'


class SubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubItem
        fields = '__all__'


class DetailItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailItem
        fields = '__all__'


class WorkRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkRecord;
        fields = '__all__'