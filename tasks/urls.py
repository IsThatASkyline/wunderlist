from django.urls import path

from .views import *

urlpatterns = [
    path('', start, name='start'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:category_id>/', TasksByCategoryView.as_view(), name='category'),
    path('category/<int:category_id>/task/<int:pk>/details', TaskDetailView.as_view(), name='view_tasks'),
    path('change_checkbox/', change_checkbox, name='change_checkbox'),
    path('create-category/', CreateCategoryView.as_view(), name='create_category'),
    path('<int:category_id>/create_task/', CreateTaskView.as_view(), name='create_task'),
    path('update-task/<int:pk>/', update_task, name='update_task'),
    path('update-task-content/', update_content, name='update_content'),
    path('<int:pk>/delete_task/', delete_task, name='delete_task'),
    path('<int:pk>/delete_category/', delete_category, name='delete_category'),
]