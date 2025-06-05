from django.contrib import admin
from .models import Company, ServiceType, Service, ServiceGeneralName

# Register your models here.
admin.site.register(Company)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(ServiceGeneralName)
