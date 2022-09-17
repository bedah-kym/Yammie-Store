from django.contrib import admin
# Register your models here.
from .models import payment_info

class PaymentAdmin(admin.ModelAdmin):

    list_display=['phone_number','amount','cart_number','user']

admin.site.register(payment_info,PaymentAdmin)
