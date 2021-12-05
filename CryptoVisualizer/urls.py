
from django.urls import path
from .views import *

urlpatterns = [
    path('crypto/', home),
    path('crypto/<str:pk>/', cryptoDetail, name='detailView'),
    path('visualizer/', generalVisualizer),
]
