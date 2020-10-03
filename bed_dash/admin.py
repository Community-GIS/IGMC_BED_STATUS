from django.contrib import admin
from .models import coordinat,doctor, UserProfile, bulk_reg
from import_export.admin import ImportExportModelAdmin
# # Register your models here.

admin.site.register(bulk_reg)

class bulkAdmin(ImportExportModelAdmin):
    list_display = ('name','email','mobile','designation','roles','from_date','to_date')