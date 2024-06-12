from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=50, blank=True, null=True)
    place_id     = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.username

class Employee(models.Model):
    username = models.CharField(max_length=50, unique=True, null=True)
    company  = models.ForeignKey(Customer, related_name="company", on_delete=models.CASCADE)

class Subscription(models.Model):
    isactive = models.BooleanField(default=False)
    company  = models.OneToOneField(Customer, related_name='subscription', on_delete=models.CASCADE)

    def status(self):
        return self.isactive