from rest_framework import serializers
from .models import TrainData


class TrainDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainData
        fields = "__all__"
        extra_kwargs={
            'train_number':{"validators": []}
        }

    def create(self,validated_data):
        train_number=validated_data.pop('train_number')

        instance,created=TrainData.objects.update_or_create(
            train_number=train_number,
            defaults=validated_data
        )
        return instance

class TrainDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrainData
        fields="__all__"