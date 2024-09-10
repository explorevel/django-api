from django.shortcuts import render
from .models import metadata, reports, institutions
from .serializers import InstitutionsSerializer, MetadataSerializer, ReportsSerializer
from rest_framework.generics import ListAPIView
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q
import pprint

# Create your views here.

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

############## below is clean ###################

class InstitutionsView(ListAPIView):
    queryset = institutions.objects.all()
    serializer_class = InstitutionsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,] 
    ###
    def list(self, request):
        cache_key = f'institution-trade: {request.query_params.get('name', None)}'
        #print(request.query_params.get('name', None))
        #cache_key = 'institution-trade'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    ###
    def get_queryset(self):
        queryset = super().get_queryset()
        institution_name = self.request.query_params.get('name', 'PT Eastspring Investment Indonesia')
        if institution_name:
            queryset = queryset.filter(Q(top_sellers__contains=[{'name': institution_name}]) | Q(top_buyers__contains=[{'name': institution_name}]))
        return queryset

class ReportsView(ListAPIView):
    queryset = reports.objects.all()
    serializer_class = ReportsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated,] 

    ###
    def list(self, request):
        cache_key = f'institution-trade: {self.request.query_params.get('name', None)}'
        #cache_key = 'reports-data'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    ###
    def get_queryset(self):
        queryset = super().get_queryset()
        reports_name = self.request.query_params.get('name', 'Banks')
        if reports_name:
            queryset = queryset.filter(sub_sector__contains=reports_name)
        return queryset

class MetadataView(ListAPIView):
    queryset = metadata.objects.all()
    serializer_class = MetadataSerializer

    ###
    def list(self, request):
        cache_key = f'institution-trade: {self.request.query_params.get('name', None)}'
        #cache_key = 'metadata-data'  # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            print(result.values())  # Log the retrieved data (for debugging purposes)
            
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
            
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
        
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

    ###
    def get_queryset(self):
        queryset = super().get_queryset()
        metadata_name = self.request.query_params.get('name', 'Banks')
        if metadata_name:
            queryset = queryset.filter(sub_sector__contains=metadata_name)
        return queryset