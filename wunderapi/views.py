from tasks.models import Tasks
from wunderapi.serializers import TaskSerializer, UserSerializer
from rest_framework import permissions, viewsets
from django.contrib.auth.models import User
from wunderapi.permissions import IsOwnerOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
   """
   This viewset automatically provides `list`, `create`, `retrieve`,
   `update` and `destroy` actions.

   Additionally we also provide an extra `highlight` action.
   """
   serializer_class = TaskSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]

   def get_queryset(self):
      return Tasks.objects.filter(user=self.request.user.id)

   def perform_create(self, serializer):
      serializer.save(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
   """
   This viewset automatically provides `list` and `retrieve` actions.
   """
   queryset = User.objects.all()
   serializer_class = UserSerializer