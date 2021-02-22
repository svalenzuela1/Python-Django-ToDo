from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import TaskViewSet, TaskItems, OneItem

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

custom_urlpatterns = [
    url(r'tasks/(?P<task_pk>\d+)/items$', TaskItems.as_view(), name='task_items'),
    url(r'tasks/(?P<task_pk>\d+)/items/(?P<pk>\d+)$', OneItem.as_view(), name='task_item')
    # url(r'tasks/(?P<task_pk>\d+)/items/(?P<pk>\d+)$', TaskViewSet.as_view())
]

urlpatterns = router.urls + custom_urlpatterns