from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Price
from .serializers import PriceSerializer

# Create your views here.

def index(request):
    return render(request, 'main/index.html')



class PriceListView(generics.ListAPIView):
    serializer_class = PriceSerializer

    def get_queryset(self):
        queryset = Price.objects.all()
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        company_id = self.request.query_params.get('company_id')
        service_id = self.request.query_params.get('service_id')
        service_type_id = self.request.query_params.get('service_type_id')

        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(max_price__lte=max_price)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if service_type_id:
            queryset = queryset.filter(service_type_id=service_type_id)

        return queryset