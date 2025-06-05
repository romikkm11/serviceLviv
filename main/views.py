from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer

# Create your views here.

def index(request):
    return render(request, 'main/index.html')



class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        # queryset = Service.objects.all()
        queryset = Service.objects.exclude(service_general_name__id=37)
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        company_id = self.request.query_params.get('company_id')
        service_type_id = self.request.query_params.get('service_type_id')
        name = self.request.query_params.get('name')
        service_general_name_id = self.request.query_params.get('service_general_name_id')

        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(max_price__lte=max_price)
        if company_id:
            queryset = queryset.filter(company__id=company_id)
        if service_type_id:
            queryset = queryset.filter(service_type__id=service_type_id)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if service_general_name_id:
            queryset = queryset.filter(service_general_name__id=service_general_name_id)
            

        return queryset