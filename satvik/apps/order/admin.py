from django.contrib import admin
import datetime
# Register your models here.
from django.urls import reverse
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

def order_name(obj):
  return '%s %s' % (obj.first_name, obj.last_name)
order_name.short_description = 'Name'

def admin_order_shipped(modeladmin, request, queryset):
  for order in queryset:
    order.status = Order.SHIPPED
    order.save()
  return
admin_order_shipped.short_description = 'Set Shipped'

def order_pdf(obj):
  return mark_safe('<a href={}>PDF</a>'.format(reverse('admin_order_pdf', args=[obj.id])))
order_name.short_description = 'PDF Title'

class OrderItemInLine(admin.TabularInline):
  model = OrderItem
  raw_id_fields = ['product'] 

class OrderAdmin(admin.ModelAdmin):
  list_display = ['id', order_name, 'status', 'created_at', order_pdf]
  list_filter = ['created_at', 'status']
  search_fields = ['first_name', 'address']
  inlines = [OrderItemInLine]
  actions = [admin_order_shipped]
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
