from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from .models import Service
from .models import Company
from .serializers import ServiceSerializer
import json, requests, math, secrets
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .geocoder.geocoder import geocode_address
import logging

# Create your views here.

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'main/index.html')

class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.filter(service_general_name__isnull=False).select_related("company", "service_type", "service_general_name")
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
    
    def get_serializer_context(self):
        auth_header = self.request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Token "):

            return super().get_serializer_context()
        else:
            context = super().get_serializer_context()
            auth_header = self.request.headers.get('Authorization')
            user_token = auth_header.replace("Token ", "").strip() if auth_header else None
            distances = cache.get(user_token)
            context["distances"] = distances 

            return context



def generate_user_token(request):
    if request.method == 'GET':
        user_token = secrets.token_urlsafe(16)
        cache.set(user_token, {}, timeout=3600)

        return JsonResponse({"token": user_token})
    else:
        return JsonResponse({"error": "Метод не дозволений"}, status=405)


def distance_calculate(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


@csrf_exempt
def return_distances(request):
    if request.method == 'POST':    
        distances = {}
        data = json.loads(request.body)
        if 'latitude' in data and 'longitude' in data:
            latitude = data.get('latitude')
            longitude = data.get('longitude')
        elif 'user_address' in data:
            address_text = data.get('user_address')
            try:
                1 / 0  # штучна помилка
            except Exception:
                logger.exception("Тест логування")
            try:
                latitude, longitude = geocode_address(address_text)
            except Exception as e:
                logger.exception("Помилка у return_distances при геокодуванні адреси")
                return JsonResponse({'error': str(e)})
        user_url = data.get('user_url')
        user_token = data.get('user_token')
        if cache.get(user_token) is not None:
            response = requests.get(user_url)
            company_ids = set()
            for i in response.json():
                company_ids.add(i['company'])
            company_coords = list(Company.objects.filter(id__in=company_ids).values('id', 'latitude', 'longititude'))
            for i in company_coords:
                dist = distance_calculate(latitude, longitude, i['latitude'], i['longititude'])
                distances[i['id']] = dist
            cache.set(user_token, distances, timeout = 3600)

            return JsonResponse({"status": "distances updated"})
        else:
            return JsonResponse({"error": "Invalid or expired token"}, status=400)


        

 


