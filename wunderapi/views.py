from tasks.models import Tasks, Category
from wunderapi.serializers import TaskSerializer, UserSerializer, CategorySerializer
from rest_framework import permissions, viewsets
from wunderapi.permissions import IsOwner
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status

from rest_framework.views import APIView

# class TaskViewSet(viewsets.ModelViewSet):
#    """
#    This viewset automatically provides `list`, `create`, `retrieve`,
#    `update` and `destroy` actions.
#
#    Additionally we also provide an extra `highlight` action.
#    """
#    serializer_class = TaskSerializer
#    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                          IsOwnerOrReadOnly]
#    authentication_classes = [TokenAuthentication]
#
#    def get_queryset(self):
#       return Tasks.objects.filter(user=self.request.user.id)
#
#    def perform_create(self, serializer):
#       serializer.save(user=self.request.user)


class TaskList(APIView):

   permission_classes = [permissions.IsAuthenticated,
                         IsOwner]
   authentication_classes = [TokenAuthentication, SessionAuthentication]


   def get(self, request):
      tasks = get_list_or_404(Tasks, user_id=request.user.id)
      serializer = TaskSerializer(tasks, many=True)
      return Response(serializer.data)


class TaskDetail(APIView):

   permission_classes = [permissions.IsAuthenticated,
                         IsOwner]
   authentication_classes = [TokenAuthentication, SessionAuthentication]

   def get(self, request, pk):
      task = get_object_or_404(Tasks, pk=pk)
      serializer = TaskSerializer(task)
      return Response(serializer.data)

   def delete(self, request, pk):
       task = get_object_or_404(Tasks, pk=pk)
       cat_id = task.category_id
       task.delete()
       return Response(cat_id)

   def patch(self, request, pk):
       task = get_object_or_404(Tasks, pk=pk)
       data = request.data
       task.title = data.get("title", task.title)
       task.is_done = data.get("is_done", task.is_done)
       task.content = data.get("content", task.content)
       task.save()
       serializer = TaskSerializer(task)

       return Response(serializer.data)


class CategoryList(APIView):

   permission_classes = [permissions.IsAuthenticated,
                         IsOwner]
   authentication_classes = [TokenAuthentication, SessionAuthentication]

   def get(self, request):
      categories = get_list_or_404(Category, user_id=request.user.id)
      serializer = CategorySerializer(categories, many=True)
      return Response(serializer.data)

   def post(self, request, *args, **kwargs):
       new_category = CategorySerializer(data=request.data)
       if new_category.is_valid():
           new_category.save(user=request.user)
       return Response(new_category.data)


class CategoryDetail(APIView):

   permission_classes = [permissions.IsAuthenticated,
                         IsOwner]
   authentication_classes = [TokenAuthentication, SessionAuthentication]
   serializer = TaskSerializer()


   def get(self, request, pk):
       tasks = get_list_or_404(Tasks, category_id=pk, user_id=request.user.id)
       serializer = TaskSerializer(tasks, many=True)
       return Response(serializer.data)


   def post(self, request, pk, *args, **kwargs):
       user = request.user.id
       task_data = request.data
       new_task = Tasks.objects.create(title=task_data['title'], category_id=pk, user_id=user)
       new_task.save()
       serializer = TaskSerializer(new_task)
       return Response(serializer.data)

   def delete(self, request, pk):
       category = get_object_or_404(Category, pk=pk)
       category.delete()
       return Response(status.HTTP_200_OK)
