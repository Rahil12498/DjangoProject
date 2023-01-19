from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.utils.text import slugify
from .models import Seller
from apps.product.models import Product
# Create your views here.

def become_seller(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)

    if form.is_valid():
      user = form.save()
      login(request, user)
      seller = Seller.objects.create(name=user.username, created_by=user)
      return redirect('frontpage')
  
  else:
    form = UserCreationForm()
  return render(request, 'seller/become_seller.html', {'form':form})

@login_required
def seller_admin(request):
  seller = request.user.seller
  products = seller.products.all()
  orders = seller.orders.all() 

  for order in orders:
    order.seller_amount = 0
    order.seller_paid_amount = 0
    order.fully_paid = True

    for item in order.items.all():
      if item.seller == request.user.seller:
          if item.seller_paid:
              order.seller_paid_amount += item.get_total_price()
          else:
              order.seller_amount += item.get_total_price()
              order.fully_paid = False

  return render(request, 'seller/seller_admin.html', {'seller': seller, 'products': products, 'orders':orders})

@login_required
def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)

    if form.is_valid():
      product = form.save(commit=False)
      product.seller = request.user.seller
      product.slug = slugify(product.title)
      product.save()
      print('valid form')
      return redirect('seller_admin')

  else:
    form = ProductForm()
  return render(request, 'seller/add_products.html',{'form': form})

@login_required
def edit_product(request, product_slug):
  product = get_object_or_404(Product, slug=product_slug)
  if request.method == 'POST':
    quantity = request.POST.get('quantity')
    product.num_available = quantity
    product.save()
    return redirect('seller_admin')
  return render(request, 'seller/edit_products.html',{'product':product})

@login_required
def edit_seller(request):
    seller = request.user.seller

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            seller.created_by.email = email
            seller.created_by.save()

            seller.name = name
            seller.save()

            return redirect('seller_admin')
    
    return render(request, 'seller/edit_seller.html', {'seller': seller})

def sellers(request):
    sellers = Seller.objects.all()

    return render(request, 'seller/sellers.html', {'sellers': sellers})

def seller(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)

    return render(request, 'seller/seller.html', {'seller': seller})