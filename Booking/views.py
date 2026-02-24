from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import BookingData
from .serializers import BookingDataSerializer,BookingListSerializer
from django.db import transaction
from Train.models import TrainData
from Users.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.conf import settings

class BookingView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self,request):
        train_number=request.data.get('train_number')
        booking_date=request.data.get('booking_date')
        seat_requested=request.data.get('seat_requested',1)

        with transaction.atomic():
            train=get_object_or_404(
                TrainData.objects.select_for_update(), 
                train_number=train_number)
            
            if train.available_seats < seat_requested:
                return Response({"error":"Not enough seats available"},status=status.HTTP_400_BAD_REQUEST)
            
            booking=BookingData.objects.create(
                user=request.user,
                train=train,
                booking_date=booking_date,
                seat_requested=seat_requested
            )
            TrainData.objects.filter(train_number=train_number).update(
                available_seats=F('available_seats') - seat_requested
            )
        serializer=BookingDataSerializer(booking)
        return Response(serializer.data,status=status.HTTP_201_CREATED)


    def get(self,request):
        booking=BookingData.objects.filter(user=request.user).select_related('train')
        serializer=BookingListSerializer(booking,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class TopRoutesAnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        pipeline = [
            {
                "$match": {
                    "params.source": {"$exists": True},
                    "params.destination": {"$exists": True}
                }
            },
            {
                "$group": {
                    "_id": {
                        "source": "$params.source",
                        "destination": "$params.destination"
                    },
                    "search_count": {"$sum": 1}
                }
            },
            {"$sort": {"search_count": -1}},
            {"$limit": 5}
        ]

        results = list(
            settings.MONGO_DB.train_search_logs.aggregate(pipeline)
        )

        formatted = [
            {
                "source": r["_id"]["source"],
                "destination": r["_id"]["destination"],
                "search_count": r["search_count"]
            }
            for r in results
        ]

        return Response(formatted)