from django.urls import path
from . import views
from helpers.commonimport import settings,static

app_name = 'pressureloss'

urlpatterns = [
    path('getallherselmodel', views.getallherselmodel, name='getallherselmodel'),
    path('calculatebitpressureloss',views.calculatebitpressureloss,name='calculatebitpressureloss'),
    path('pressurelosschart',views.pressurelosschart,name='pressurelosschart'),
    path('calculate_annular_drillstring_loss',views.calculate_annular_drillstring_loss,name='calculate_annular_drillstring_loss'),
    path('calculate_cci_trans_cutting',views.calculate_cci_trans_cutting,name='calculate_cci_trans_cutting'),
    path('ecdbitdepth_calculation',views.ecdbitdepth_calculation,name='ecdbitdepth_calculation'),
    path('ecdalongwell_calculation',views.ecdalongwell_calculation,name='ecdalongwell_calculation'),
    path('download_pressurelosschart/<str:chart_type>/<int:wellphase_id>/',views.DownloadPressurelossChart.as_view(),name='download_pressurelosschart'),
    path('getallbingham',views.getallbingham,name='getallbingham'),
    path('getallpowerlaw',views.getallpowerlaw,name='getallpowerlaw'),
    path('sensitivity_calculation',views.sensitivity_calculation,name='sensitivity_calculation'),
    path('calculate_slipvelocity',views.calculate_slipvelocity,name='calculate_slipvelocity'),
    path('setsession',views.setsession,name='setsession'),
    path('generate_phase_report/<int:wellphase_id>/',views.generate_phase_report,name='generate_phase_report'),
    path('calculatesurfacelosses',views.calculatesurfacelosses,name='calculatesurfacelosses'),
    path('generate_totalwell_report/<int:wellphase_id>/',views.generate_totalwell_report,name='generate_totalwell_report'),
    path('sensitivity_report/<int:wellphase_id>/',views.sensitivity_report,name='sensitivity_report'),
    path('calculateoptimization',views.calculateoptimization,name='calculateoptimization'),




]