from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views
from app.views import create_work_record, detail_view, index, subitem_view
from app.viewsets import (DetailItemViewSet, MajorItemViewSet, SubItemViewSet,
                          WorkRecordViewSet, WorkRecordByDateViewSet, WorkRecordSummaryView, MonthBonusViewSet)
from django.contrib.auth import views as auth_views

app_name = 'app'
# Restful api
router = DefaultRouter()
router.register('major', viewset=MajorItemViewSet),
router.register(r'subitem/(?P<major_id>\d+)', SubItemViewSet, basename='subitem'),
# router.register('subitem/<int:major_id>/',viewset=SubItemViewSet,basename='subitem'),
router.register(r'detail/(?P<subitem_id>\d+)', DetailItemViewSet, basename='detail'),
router.register(r'workrecord/(?P<detail_id>\d+)', WorkRecordViewSet, basename='workrecord'),
router.register(r'workrecord/(?P<working_date>\d{4}-\d{2}-\d{2})', WorkRecordByDateViewSet,
                basename='workrecord_by_date'),

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('dashboard', views.dashboard, name='dashboard'),  # 首頁 dashboard
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 首頁 login
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'), # 首頁 logout
    path('register/', views.register, name='register'),
    path('report/<int:year>/<int:month>', views.report, name='report'),  # 月報總表
    path('person-report/<int:year>/<int:month>', views.person_report, name='person_report'), # 個人月報總表
    path('sub_view/<int:id>', subitem_view, name='sub_view'),
    path('detail_view/<int:id>', detail_view, name='detail_view'),
    path('create_work_record/<int:id>', create_work_record, name='create_work_record'),
    path('api/summary/<int:user_id>/<str:working_date>/', WorkRecordSummaryView.as_view({'get': 'summary'}),
         name='workrecord-summary'),
]
