from django.db import models

from customer.models import Customer

class FeedBack(models.Model):
    author_name = models.CharField(max_length=50, blank=True, null=True)
    employee = models.CharField(max_length=50, blank=True, null=True)
    callback = models.CharField(max_length=50, blank=True, null=True)
    text_info = models.CharField(max_length=50, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    insertion_time = models.DateTimeField(auto_now_add=True)
    company  = models.ForeignKey(Customer, related_name="business", on_delete=models.CASCADE)
