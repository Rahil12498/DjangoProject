from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.cart.cart import Cart

from .models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, zipcode, place, phone, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, place=place, phone=phone, paid_amount=amount, customer=request.user.customer)


    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], seller=item['product'].seller, price=item['product'].price, quantity=item['quantity'])
        item['product'].num_available = int(item['product'].num_available) - int(item['quantity'])
        item['product'].save()
        order.sellers.add(item['product'].seller)

    return order

def notify_seller(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for seller in order.sellers.all():
        to_email = seller.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_seller.html', {'order': order, 'seller': seller})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def notify_seller_delete(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    for item in order.items.all(): 
        to_email = item.seller.created_by.email
        subject = 'Order Cancelled'
        text_content = 'Your Order has been deleted'
        html_content = render_to_string('order/email_notify_seller.html', {'order': order, 'seller': item.seller})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer_delete(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.email
    subject = 'Order Cancellation Confirmation'
    text_content = 'Your Order has been successfully cancelled'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()