from django.urls import path
from .views import *

urlpatterns = [

    path('api/buttons', FirstButtons.as_view(), name='first-buttons'),
    path('api/query', QueryResult.as_view(), name='query'),
    path('api/notify', NotificationInfo.as_view(), name='notify'),

]
