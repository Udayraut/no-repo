from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index_view, name='index'),
    path('export/posts/csv/', views.export_posts_csv, name='export_posts_csv'),
    path('export/posts/excel/', views.export_posts_excel, name='export_posts_excel'),
    path('export/playstore/csv/', views.export_playstore_csv, name='export_playstore_csv'),
    path('export/daily-logs/csv/', views.export_daily_logs_csv, name='export_daily_logs_csv'),
]
