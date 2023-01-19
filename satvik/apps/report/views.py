
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from apps.seller.models import Seller
from apps.product.models import Product
from apps.order.models import Order
from datetime import datetime
import pytz

# Create your views here.

@login_required
def get_report(request):
  utc = pytz.UTC

  seller = request.user.seller
  products = seller.products.all()
  orders = seller.orders.all() 

  if request.method == 'POST':
    to_date = request.POST.get('to_date')
    from_date = request.POST.get('from_date')
    time = request.POST.get('time')
    if time == 'monthly':
      currentMonth = datetime.now().month 
      month_orders = set()
      for order in orders:
        if order.created_at.month == currentMonth:
          month_orders.add(order)
      return render(request, 'report.html', {'seller': seller, 'products': products, 'orders':month_orders})
    elif time == 'yearly':
      currentYear = datetime.now().year 
      year_orders = set()
      for order in orders:
        if order.created_at.year == currentYear:
          year_orders.add(order)
      return render(request, 'report.html', {'seller': seller, 'products': products, 'orders':year_orders})
    elif time == 'daily':
      currentDay = datetime.now().strftime("%d/%m/%Y") 
      daily_orders = set()
      for order in orders:
        if order.created_at.strftime("%d/%m/%Y") == currentDay:
          daily_orders.add(order)
      return render(request, 'report.html', {'seller': seller, 'products': products, 'orders':daily_orders})
    elif time == 'nothing':
      if to_date and from_date:
        date_orders = set()
        start_date = datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.strptime(to_date, "%Y-%m-%d")
        for order in orders:
          if (order.created_at >= start_date.replace(tzinfo=utc)) and (order.created_at <= end_date.replace(tzinfo=utc)):
            date_orders.add(order)
      return render(request, 'report.html', {'seller': seller, 'products': products, 'orders':date_orders})

  return render(request, 'report.html')