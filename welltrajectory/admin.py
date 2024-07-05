from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import WellTrajectory

# Register your models here.
class WellTrajectoryAdmin(ImportExportModelAdmin):
    list_display = ('measured_depth', 'inclination', 'azimuth','true_vertical_depth','dls')