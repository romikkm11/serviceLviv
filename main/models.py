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
    
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Послуга')

    def __str__(self):
        return self.name
    
class Price(models.Model):
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        if self.max_price:
            return f"Компанія: {self.company.name}, Тип: {self.service_type.name}, Послуга: {self.service.name}, Від: {self.min_price}, До: {self.max_price}"
        else:
            return f"Компанія: {self.company.name}, Тип: {self.service_type.name}, Послуга: {self.service.name}, Від: {self.min_price}"
