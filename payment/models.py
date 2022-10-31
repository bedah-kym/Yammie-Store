from django.db import models
from Shop.models import Cart
from django.contrib.auth.models import User

# Create your models here.
class payment_info(models.Model):
    phone_number = models.IntegerField()
    amount = models.IntegerField(default=0)
    cart_number = models.ForeignKey(Cart,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20,default='none')
    paid_on = models.DateTimeField(auto_now_add=True)
    street = models.CharField(max_length=100,default='none')
    location = models.CharField(max_length=100,default='none')
    #County = models.CharField(max_length=100,default='None')
    class Meta:
        verbose_name_plural="Mpesa Payments"
