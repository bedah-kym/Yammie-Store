from django.contrib import admin
# Register your models here.
from .models import payment_info

class PaymentAdmin(admin.ModelAdmin):

    list_display=['user','phone_number','amount','cart_number','paid_on']


admin.site.register(payment_info,PaymentAdmin)
