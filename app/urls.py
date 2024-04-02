from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views
from app.views import create_work_record, detail_view, index, subitem_view, work_record,todo_list
from app.viewsets import (DetailItemViewSet, MajorItemViewSet, SubItemViewSet,
                          WorkRecordViewSet, WorkRecordByDateViewSet, WorkRecordSummaryView, MonthBonusViewSet,
                          WorkoutViewSet, ToDoViewSet)
from django.contrib.auth import views as auth_views

app_name = 'app'
# Restful api
router = DefaultRouter()
router.register('major', viewset=MajorItemViewSet),
router.register('todo', viewset=ToDoViewSet),
router.register(r'subitem/(?P<major_id>\d+)', SubItemViewSet, basename='subitem'),
router.register(r'detail/(?P<subitem_id>\d+)', DetailItemViewSet, basename='detail'),
# jobs.js 的 save() 使用
router.register(r'workrecord/(?P<detail_id>\d+)', WorkRecordViewSet, basename='workrecord'),
router.register(r'workrecord/(?P<working_date>\d{4}-\d{2}-\d{2})', WorkRecordByDateViewSet,
                basename='workrecord_by_date'),


urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('dashboard', views.dashboard, name='dashboard'),  # 首頁 dashboard
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 首頁 login
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='logout'),  # 首頁 logout
    path('register/', views.register, name='register'),
    path('report/<int:year>/<int:month>', views.report, name='report'),  # 月報總表
    path('person-report/<int:year>/<int:month>', views.person_report, name='person_report'),  # 個人月報總表
    path('sub_view/<int:id>', subitem_view, name='sub_view'),
    path('detail_view/<int:id>', detail_view, name='detail_view'),
    path('create_work_record/<int:id>', create_work_record, name='create_work_record'),
    path('api/summary/<int:user_id>/<str:working_date>/', WorkRecordSummaryView.as_view({'get': 'summary'}),
         name='workrecord-summary'),
    # 檢查該時段是否有資料
    path('api/working/<int:user_id>/<str:working_date>/<str:start_time>/<str:end_time>/',
         WorkoutViewSet.as_view({'get': 'check'}), name='workout'),
    path('work_record/<slug:work>/', work_record, name='work_record'),
    path('todo_list/',todo_list, name='todo_list')

]
