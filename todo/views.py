from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import (ValidationError, PermissionDenied)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TaskSerializer, ItemSerializer
from .models import Task, Item


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    #GET ALL TASKS
    def get_queryset(self):
        queryset = Task.objects.all().filter(user=self.request.user).order_by('created_at')
        return queryset

    #POST TASK
    def create(self, request, *args, **kwargs):
        task = Task.objects.filter(
            name=request.data.get('name'),
            user=request.user
        )

        if task:
            message = 'Task already exists.'
            raise ValidationError(message)
        return super().create(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #DELETE TASK
    def destroy(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        if not request.user == task.user:
            raise PermissionDenied('Failed To Delete Task')

        super().destroy(request, *args, **kwargs)
        return Response({
            'message': 'Task Has Been Deleted'
        })

class TaskItems(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    #GET ALL ITEMS FROM TASK
    def get_queryset(self):
        try:
            if self.kwargs.get('task_pk'):
                task = Task.objects.get(pk=self.kwargs["task_pk"])
                queryset = Item.objects.filter(
                    task=task,
                    user=self.request.user
                ).order_by('created_at')
                if not queryset:
                    raise ValidationError('No Access To This Task')
                else:
                    return queryset
        except Task.DoesNotExist:
            raise ValidationError('No Access To This Task')

    #POST TASK
    def create(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.request.data['task']):
                return super().create(request)
        except Task.DoesNotExist:
            raise ValidationError('Not Able To Add Within Task Selected')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OneItem(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
#GET ALL ITEMS
    def get_queryset(self):
        try:
            if self.kwargs.get('task_pk') and self.kwargs.get('pk'):
                task = Task.objects.get(pk=self.kwargs['task_pk'])
                queryset = Item.objects.filter(
                    task=task,
                    user=self.request.user,
                    pk=self.kwargs['pk']
                )
                return queryset
        except Task.DoesNotExist:
            raise ValidationError("Item Doesn't Exist, Try Again")
#POST ITEMS
    def create(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.request.data['item']):
                return super().create(request)
        except Task.DoesNotExist:
            raise ValidationError('Not Able To Add Item')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.request.data['task']):
                return super().update(request, *args, **kwargs)
        except Task.DoesNotExist:
            raise ValidationError('Failure To Update Item In Task')

    def destroy(self, request, *args, **kwargs):
        try:
            if self.request.user.tasks.get(pk=self.kwargs['task_pk']):
                super().destroy(request, *args, **kwargs)
                return Response({
                    "message": "Item Deleted."
                })
        except Task.DoesNotExist:
            raise ValidationError('Failure To Delete Item In Task')