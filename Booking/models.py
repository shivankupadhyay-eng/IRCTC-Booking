from django.db import models
from Users.models import CustomUser
from Train.models import TrainData
import uuid


class BookingData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='custom_user')
    train=models.ForeignKey(TrainData, on_delete=models.CASCADE,related_name='train')
    booking_date=models.DateField()
    seat_requested=models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'train', 'booking_date')
        verbose_name="Booking Data"
        verbose_name_plural="Booking Data"