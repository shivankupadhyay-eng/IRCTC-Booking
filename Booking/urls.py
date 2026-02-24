from django.urls import path
from .views import BookingView,TopRoutesAnalyticsAPIView

urlpatterns = [
    path('', BookingView.as_view(), name='booking-list'),
    path('create/', BookingView.as_view(), name='booking-create'),
    path("analytics/top-routes/", TopRoutesAnalyticsAPIView.as_view()),
]
