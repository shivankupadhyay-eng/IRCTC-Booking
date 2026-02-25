from rest_framework import serializers
from .models import BookingData
from Train.serializers import TrainDataListSerializer

class BookingDataSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    train_number = serializers.CharField(source='train.train_number', read_only=True)
    class Meta:
        model = BookingData
        fields = ['id', 'user_email', 'train_number', 'booking_date', 'seat_requested']

class BookingListSerializer(serializers.ModelSerializer):
    train = TrainDataListSerializer(read_only=True)
    class Meta:
        model = BookingData
        fields = ['train', 'booking_date', 'seat_requested']