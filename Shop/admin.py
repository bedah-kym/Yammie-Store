from django.contrib import admin
from .models import Cart,CartItem,Item
# Register your models here.
class CartItemTubular(admin.TabularInline):

    model = CartItem

class CartAdmin(admin.ModelAdmin):
    fieldsets=[
    ('product',{"fields":['items']}),
    ('is the order paid ?',{"fields":['ordered']}),
    ('payment reference code',{"fields":['ref_code']}),
    ('deliverly location',{"fields":['county','location','street_name']}),

    ]
    inlines=[]
    list_display=['owner','order_date','ordered']
    filter_by=['owner','order_date','ordered']


admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem)
admin.site.register(Item)
