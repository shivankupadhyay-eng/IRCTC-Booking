from django.contrib import admin
from .models import TrainData

@admin.register(TrainData)
class TrainDataAdmin(admin.ModelAdmin):
    list_display = ('id','train_number', 'name', 'source', 'destination', 'departure_time', 'arrival_time', 'total_seats', 'available_seats')
    search_fields = ('train_number', 'name', 'source', 'destination')
    list_filter = ('source', 'destination')