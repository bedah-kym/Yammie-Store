from django.contrib import admin
from .models import Cart,Item
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display=['title','weight','price','in_stock']
    list_filter=['category']


class CartAdmin(admin.ModelAdmin):
    fieldsets=[
    ('product',{"fields":['items']}),
    ('is the order paid ?',{"fields":['ordered']}),
    ('payment reference code',{"fields":['ref_code']}),
    ('payment info',{"fields":['payment_method','total_price']}),
    ('deliverly info ',{"fields":['owner','user_phone','county','location','street_name']}),
    ('has the client been called ?',{"fields":['agent_confirmed']})
    ]
    inlines= []
    list_display = ['owner','order_date','ordered','payment_method','agent_confirmed']
    list_filter =  ['payment_method','order_date']


admin.site.register(Cart,CartAdmin)
admin.site.register(Item,ItemAdmin)
