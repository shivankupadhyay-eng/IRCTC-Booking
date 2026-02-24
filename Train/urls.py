from django.urls import path
from .views import TrainDataView, TrainSearchView

urlpatterns = [
    path('trains/search/', TrainSearchView.as_view(), name='train-search'),
    path('trains/', TrainDataView.as_view(), name='train-list'),
    path('trains/<str:train_number>/', TrainDataView.as_view(), name='train-detail'),
]
