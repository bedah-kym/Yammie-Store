from django.contrib import admin
from .models import Cart,CartItem,Item
# Register your models here.
class CartItemTubular(admin.TabularInline):
    model = CartItem

class CartAdmin(admin.ModelAdmin):
    fieldsets=[
    ('product',{"fields":['items']}),
    ('is the order paid ?',{"fields":['ordered']}),
    #('Date Ordered',{"fields":['order_date']}),

    ]
    inlines=[]
    list_display=['owner','order_date','ordered']


admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem)
admin.site.register(Item)
