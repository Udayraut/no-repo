from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('posts/', views.post_list_view, name='post_list'),
    path('posts/new/', views.post_create_view, name='post_create'),
    path('posts/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_update_view, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete_view, name='post_delete'),
    path('posts/<int:post_pk>/metric/new/', views.metric_create_view, name='metric_create'),
    path('daily-log/', views.daily_log_view, name='daily_log'),
    path('calendar/', views.calendar_view, name='calendar'),
]
