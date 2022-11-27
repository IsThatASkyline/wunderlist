from django.urls import path, include
from wunderapi import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'tasks', views.TaskViewSet, basename='tasks')
# router.register(r'users', views.UserViewSet, basename='users')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('tasks/', views.TaskList.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
]
