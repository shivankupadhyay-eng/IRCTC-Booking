from django.contrib import admin
from .models import BookingData

@admin.register(BookingData)
class BookingDataAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'train', 'booking_date', 'seat_requested')
    search_fields = ('user__email', 'train__train_number')
    list_filter = ('booking_date',)