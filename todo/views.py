from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.generics import GenericAPIView
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

    def update(self, request, *args, **kwargs):
        try:
            if self.request.user.item.get(pk=self.request.data['task']):
                return super().update(request, *args, **kwargs)
        except Item.DoesNotExist:
            raise ValidationError('Failure To Update Item In Task')

    #DELETE TASK
    def destroy(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs['pk'])
        if not request.user == task.user:
            raise PermissionDenied('You are not authorized to delete task')

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
            raise ValidationError('Task Does Not Exist')

    #POST TASK
    # def create(self, request, *args, **kwargs):
    #     try:
    #         if self.request.user.tasks.get(pk=self.request.data['task']):
    #             return super().create(request)
    #     except Task.DoesNotExist:
    #         raise ValidationError('Not Able To Add Within Task Selected')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OneItem(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

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

        except Item.DoesNotExist:
            raise ValidationError("Item Doesn't Exist, Try Again")


    # def create(self, request, *args, **kwargs):
    #     try:
    #         return super().create(request, *args, **kwargs)
    #
    #     except request.user.is_anonymous:
    #
    #         raise PermissionDenied("Only logged in users can create Items")
    #
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #
    #
    # def destroy(self, request, *args, **kwargs):
    #
    #     item = Item.objects.get(pk=self.kwargs["pk"])
    #
    #     try:
    #         return super().destroy(request, *args, **kwargs)
    #
    #     except request.user != item.user:
    #         raise PermissionDenied(
    #             "You do not have the access to delete this item"
    #         )


class ItemViewSet(viewsets.ModelViewSet):
# class ItemViewSet(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def  get_serializer_class(self):

            """
           Return the class to use for the serializer.
           Defaults to using `self.serializer_class`.

           You may want to override this if you need to provide different
           serializations depending on the incoming request.

           (Eg. admins get full serialization, others get basic serialization)
           """


            assert (
                self.serializer_class is not None
                or self.serializer_class_mapping is not None
            ), (
        "'%s' should either include a `serializer_class` attribute or "
        "a `serializer_class_mapping` attribute, "
        "or override the `get_serializer_class()` method." % self.__class__.__name__
            )

            if self.serializer_class_mapping:
                return self.serializer_class_mapping[self.request.method]
            return self.serializer_class


    def get_queryset(self):
        try:
            queryset = Item.objects.all().filter(user=self.request.user)
            return queryset
        except Item.DoesNotExist:
            raise ValidationError("Item Does Not Exist. Try Again")


    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)

        except request.user.is_anonymous:

            raise PermissionDenied("Only logged in users can create Items")


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):

        item = Item.objects.get(pk=self.kwargs["pk"])

        try:
            return super().destroy(request, *args, **kwargs)

        except request.user != item.user:
            raise PermissionDenied(
                "You do not have the access to delete this item"
            )
# #POST ITEMS
#     def create(self, request, *args, **kwargs):
#         try:
#             if self.request.user.item.get(pk=self.request.data['item_pk']):
#                 return super().create(request)
#         except Item.DoesNotExist:
#             raise ValidationError('Not Able To Add Item')
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
#     def update(self, request, *args, **kwargs):
#         try:
#             if self.request.user.item.get(pk=self.request.data['task']):
#                 return super().update(request, *args, **kwargs)
#         except Item.DoesNotExist:
#             raise ValidationError('Failure To Update Item In Task')
#
#     def destroy(self, request, *args, **kwargs):
#         try:
#             if self.request.user.item.get(pk=self.kwargs['item_pk']):
#                 super().destroy(request, *args, **kwargs)
#                 return Response({
#                     "message": "Item Deleted."
#                 })
#         except Item.DoesNotExist:
#             raise ValidationError('Failure To Delete Item In Task')