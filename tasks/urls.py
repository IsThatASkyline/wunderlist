from django.urls import path

from .views import *

urlpatterns = [
    path('', start, name='start'),
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    # path('<int:category_id>/', view_category, name='category'),
    path('<int:category_id>/', TasksByCategoryView.as_view(), name='category'),
    # path('<int:category_id>/<int:pk>/details', detail_task, name='view_tasks'),
    path('<int:category_id>/<int:pk>/details', TaskDetailView.as_view(), name='view_tasks'),
    path('change_checkbox/', change_checkbox, name='change_checkbox'),
    path('create-category/', create_category, name='create_category'),
    # path('<int:category_id>/create_task/', create_task, name='create_task'),
    path('<int:category_id>/create_task/', CreateTaskView.as_view(), name='create_task'),
    path('update-task/<int:pk>/', update_task, name='update_task'),
    path('update-task-content/', update_content, name='update_content'),
    path('<int:pk>/delete_task/', delete_task, name='delete_task'),
    path('<int:pk>/delete_category/', delete_category, name='delete_category'),

    # path('<int:pk>/details', HomeDetails.as_view(), name='home_details'),
    # path('tasks/add-task/', add_task, name='add_task'),
    # path('tasks/create-task/', create_task, name='create-task'),
    # path('tasks/<int:task_id>/', view_tasks, name='view_tasks'),
    # path('<int:category_id>/<int:pk>/details', ViewTasks.as_view(), name='view_tasks'),
    # path('category/<str:category_title>/', get_category, name='category'),
    # path('<int:category_id>/', TasksByCategory.as_view(), name='category'),
    # path('', index, name='home'),
    # path('id/', get_user_id, name='id'),
]