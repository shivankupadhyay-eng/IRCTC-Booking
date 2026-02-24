from django.db import models
import uuid

class TrainData(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    train_number=models.CharField(max_length=5,unique=True,db_index=True)
    name=models.CharField(max_length=100)
    source=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    departure_time=models.DateTimeField()
    arrival_time=models.DateTimeField()
    total_seats=models.IntegerField()
    available_seats=models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name="Train Data"
        verbose_name_plural="Train Data"
        unique_together = ('train_number','name')