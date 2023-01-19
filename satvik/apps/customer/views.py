from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from apps.product.models import Product
from apps.order.models import Order
from django.utils.text import slugify
from apps.order.utilities import notify_seller_delete,notify_customer_delete
# Create your views here.

def signup(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)

    if form.is_valid():
      user = form.save()
      login(request, user)
      customer = Customer.objects.create(name=user.username, created_by=user)
      return redirect('frontpage')
  
  else:
    form = UserCreationForm()
  return render(request, 'customer/signup.html', {'form':form})

@login_required
def customer_account(request):
  customer = request.user.customer
  orders = customer.orders.all
  return render(request, 'customer/customer_account.html', {'customer':customer, 'orders':orders})

@login_required
def edit_customer(request):
  customer = request.user.customer

  if request.method == 'POST':
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        if last_name:
            customer.email = email
            customer.last_name = last_name
            customer.address = address
            customer.save()

            return redirect('customer_account')
    
  return render(request, 'customer/edit_customer.html', {'customer': customer})

@login_required
def delete_order(request, order_id):
  customer = request.user.customer
  order = get_object_or_404(Order, pk=order_id)
  notify_seller_delete(order)
  notify_customer_delete(order)
  order.delete()
  orders = customer.orders.all
  
  return render(request, 'customer/customer_account.html', {'customer':customer, 'orders':orders, 'order':order})
