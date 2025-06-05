from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    latitude = models.FloatField(verbose_name = "Широта", null = True, blank = True)
    longititude = models.FloatField(verbose_name = "Довгота", null = True, blank = True)

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=200, verbose_name='Тип послуги')

    def __str__(self):
        return self.name
    
class ServiceGeneralName(models.Model):
    name = models.CharField(max_length=200, verbose_name='Загальна назва послуги')

    def __str__(self):
        return self.name
    
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Послуга')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null = True, blank = True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null = True, blank = True)
    service_general_name = models.ForeignKey(ServiceGeneralName, on_delete=models.SET_NULL, verbose_name='Узагальнена послуга', null = True, blank = True)

    def __str__(self):
        return self.name
