from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=False, methods=['delete'])
    def completed(self, request):
        count, _ = Todo.objects.filter(completed=True).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
