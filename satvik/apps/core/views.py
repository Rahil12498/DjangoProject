from django.shortcuts import render
from apps.product.models import Product
# Create your views here.

def frontpage(request):
  new_products = Product.objects.all()[0:8]
  return render(request, 'core/frontpage.html', {'new_products': new_products})

def contact(request):
  return render(request, 'core/contact.html')