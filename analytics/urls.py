from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_overview_view, name='overview'),
    path('playstore/', views.playstore_list_view, name='playstore_list'),
    path('playstore/new/', views.playstore_create_view, name='playstore_create'),
    path('playstore/<int:pk>/delete/', views.playstore_delete_view, name='playstore_delete'),
    path('goals/', views.goal_list_view, name='goal_list'),
    path('goals/new/', views.goal_create_view, name='goal_create'),
    path('goals/<int:pk>/edit/', views.goal_update_view, name='goal_update'),
    path('goals/<int:pk>/delete/', views.goal_delete_view, name='goal_delete'),
]
