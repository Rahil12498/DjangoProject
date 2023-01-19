import random
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Productreview
from .forms import AddToCartForm
from django.contrib import messages
# Create your views here.

from apps.cart.cart import Cart

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'product/search.html', {'products': products, 'query': query})


def product(request, category_slug, product_slug):
    cart = Cart(request)
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.method == 'POST':
        
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product was added to the cart')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)
        
        content = request.POST.get('content', '')
        rating = request.POST.get('rating', 3)
        review = Productreview.objects.create(product=product, customer = request.user.customer, rating=rating, content=content)
        return redirect('product', category_slug=category_slug, product_slug=product_slug)

    else:
        form = AddToCartForm()


    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)
    
    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    return render(request, 'product/product.html', {'product': product, 'similar_products': similar_products, 'form':form})

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'product/category.html', {'category': category})