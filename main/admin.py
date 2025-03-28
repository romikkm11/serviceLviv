from django.contrib import admin
from .models import Company, ServiceType, Service, Price

# Register your models here.
admin.site.register(Company)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Price)