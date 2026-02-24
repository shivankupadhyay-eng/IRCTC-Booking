from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TrainData
from .serializers import TrainDataCreateSerializer,TrainDataListSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
import time
from datetime import datetime
from django.conf import settings

class TrainDataView(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    def post(self, request):
        serializer=TrainDataCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def get(self, request,train_number):
        if id:
            train=get_object_or_404(TrainData,train_number=train_number)
            serializer=TrainDataListSerializer(train)
            return Response(serializer.data,status=status.HTTP_200_OK)
        queryset=TrainData.objects.all()
        serializer=TrainDataListSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class TrainSearchView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        start_time=time.time()
        source=request.query_params.get("source")
        destination=request.query_params.get("destination")
        date=request.query_params.get("date")
        try:
            limit=int(request.query_params.get("limit", 10))
            offset=int(request.query_params.get("offset", 0))
        except ValueError:
            return Response({"error": "limit and offset must be integers"}, status=400)
        queryset=TrainData.objects.filter(
            source__iexact=source,
            destination__iexact=destination
        )

        if date:
            queryset=queryset.filter(departure_time__date=date)
        total_results=queryset.count()
        queryset=queryset[offset:offset+limit]
        serializer=TrainDataListSerializer(queryset,many=True)
        execution_time=(time.time()-start_time)*1000

        settings.MONGO_DB.train_search_logs.insert_one(
            {
                "endpoint":"/api/trains/search",
                "params":{
                    "source":source,
                    "destination":destination,
                    "date":date,
                    "limit":limit,
                    "offset":offset
                },
                "user_id":str(request.user.id),
                "execution_time_ms":execution_time,
                "result_count":total_results,
                "timestamp":datetime.utcnow()  
})
        return Response(
            {
                "count":total_results,
                "results":serializer.data
            }
        )