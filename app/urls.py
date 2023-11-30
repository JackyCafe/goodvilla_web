from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.views import create_work_record, detail_view, index, subitem_view
from app.viewsets import (DetailItemViewSet, MajorItemViewSet, SubItemViewSet,
                          WorkRecordViewSet, WorkRecordByDateViewSet, WorkRecordSummaryView)

app_name='app'
router = DefaultRouter()
router.register('major',viewset=MajorItemViewSet),
router.register(r'subitem/(?P<major_id>\d+)', SubItemViewSet, basename='subitem'),
# router.register('subitem/<int:major_id>/',viewset=SubItemViewSet,basename='subitem'),
router.register(r'detail/(?P<subitem_id>\d+)', DetailItemViewSet, basename='detail'),
router.register(r'workrecord/(?P<detail_id>\d+)',WorkRecordViewSet,basename='workrecord'),
router.register(r'workrecord/(?P<working_date>\d{4}-\d{2}-\d{2})',WorkRecordByDateViewSet,basename='workrecord_by_date'),



urlpatterns = [
    path('', index,name='index'),
    path('sub_view/<int:id>', subitem_view,name='sub_view'),
    path('detail_view/<int:id>', detail_view,name='detail_view'),
    path('create_work_record/<int:id>', create_work_record,name='create_work_record'),
    path('api/',include(router.urls)),
    path('api/summary/<str:working_date>/', WorkRecordSummaryView.as_view({'get': 'summary'}),
         name='workrecord-summary'),

]
