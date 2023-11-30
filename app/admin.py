from django.contrib import admin

# Register your models here.
from django.contrib import admin

from app.models import MajorItem,SubItem,DetailItem,WorkRecord


# Register your models here.

@admin.register(MajorItem)
class MajorItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MajorItem._meta.fields]


@admin.register(SubItem)
class SubItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SubItem._meta.fields]


@admin.register(DetailItem)
class DetailAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DetailItem._meta.fields]


@admin.register(WorkRecord)
class WorkRecordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WorkRecord._meta.fields]