from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import TaskViewSet, TaskItems, OneItem, ItemViewSet

router = routers.DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'items', ItemViewSet, basename='items')

custom_urlpatterns = [
    url(r'tasks/(?P<task_pk>\d+)/items$', TaskItems.as_view(), name='task_items'),
    url(r'tasks/(?P<task_pk>\d+)/items/(?P<pk>\d+)$', OneItem.as_view(), name='one_item')
    # url(r'tasks/items/', ItemViewSet.as_view(), name='item')
    # url(r'tasks/(?P<task_pk>\d+)/items/(?P<pk>\d+)$', TaskViewSet.as_view())
]

urlpatterns = router.urls
urlpatterns += custom_urlpatterns
