from tasks.models import Tasks, Category
from wunderapi.serializers import TaskSerializer, UserSerializer, CategorySerializer
from rest_framework import permissions, viewsets
from django.contrib.auth.models import User
from wunderapi.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404

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

   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]
   authentication_classes = [TokenAuthentication, SessionAuthentication]

   def get(self, request):
      tasks = Tasks.objects.filter(user_id=request.user.id)
      serializer = TaskSerializer(tasks, many=True)
      return Response(serializer.data)


class TaskDetail(APIView):

   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]
   authentication_classes = [TokenAuthentication, SessionAuthentication]

   def get_object(self, pk):
      try:
         return Tasks.objects.get(pk=pk)
      except Tasks.DoesNotExist:
         raise Http404

   def get(self, request, pk):
      task = self.get_object(pk)
      serializer = TaskSerializer(task)
      return Response(serializer.data)

   def patch(self, request, pk):
       try:
          task = self.get_object(pk)
       except:
          raise Http404

       data = request.data

       task.title = data.get("title", task.title)
       task.is_done = data.get("is_done", task.is_done)
       task.content = data.get("content", task.content)
       task.save()
       serializer = TaskSerializer(task)

       return Response(serializer.data)


class CategoryList(APIView):

   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]
   authentication_classes = [TokenAuthentication, SessionAuthentication]

   def get(self, request):
      categories = Category.objects.filter(user_id=request.user.id)
      serializer = CategorySerializer(categories, many=True)
      return Response(serializer.data)

   def post(self, request, *args, **kwargs):
       new_category = CategorySerializer(data=request.data)
       if new_category.is_valid():
           new_category.save()
       return Response(new_category.data)


class CategoryDetail(APIView):

   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]
   authentication_classes = [TokenAuthentication, SessionAuthentication]
   serializer = TaskSerializer()


   def get(self, request, pk):
       category = Category.objects.get(pk=pk)
       if category.user_id == request.user.id:
           tasks = Tasks.objects.filter(category_id=pk, user_id=request.user.id)
           serializer = TaskSerializer(tasks, many=True)
           return Response(serializer.data)
       else:
           raise Http404

   def post(self, request, pk, *args, **kwargs):
       user = request.user.id
       task_data = request.data
       new_task = Tasks.objects.create(title=task_data['title'], category_id=pk, user_id=user, content=task_data['content'])
       new_task.save()
       serializer = TaskSerializer(new_task)
       return Response(serializer.data)




#
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#    """
#    This viewset automatically provides `list` and `retrieve` actions.
#    """
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    authentication_classes = [TokenAuthentication]
