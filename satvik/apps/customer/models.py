from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
   name = models.CharField(max_length=225)
   last_name = models.CharField(max_length=225)
   email = models.CharField(max_length=225)
   address = models.CharField(max_length=225)
   created_at = models.DateTimeField(auto_now_add=True)
   created_by = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE)

   class Meta:
      ordering = ['name']
    
   def __str__(self):
      return self.name