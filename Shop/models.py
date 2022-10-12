from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

CATEGORY_CHOICES=[
    ('cow products','for cows'),
    ('chicken products','for chicken'),
    ('pig products','for pigs'),
    ('general feeds','for any')
]
class Item(models.Model):
    title = models.CharField(max_length=50)
    weight = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=30)
    description = models.TextField(default=True)
    in_stock = models.BooleanField(default=True)
    discount = models.IntegerField(default=0)
    item_image = models.ImageField(null=False,upload_to="product_pics")


    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse('Shop:add_to_cart', kwargs={'product_id' : self.pk})

    def get_remove_from_cart_url(self):
        return reverse('Shop:remove_from_cart', kwargs={'product_id' : self.pk})

    def save(self):
        super().save()
        img = Image.open(self.item_image.path)
        if img.width > 100 or img.height > 100:
            outputsize=(200,200)
            img.thumbnail(outputsize)
            img.save(self.item_image.path)



class CartItem (models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} bag(s) of {self.item.weight}kg {self.item}"
    def get_item_total_price(self):
        return self.item.price * self.quantity

    def get_item_discount_price(self):
        return self.item.discount *self.quantity


class Cart(models.Model):
    items = models.ManyToManyField(CartItem)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    total_price = models.IntegerField(default=0)
    ref_code = models.CharField(max_length=30)
    street_name= models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20)
    agent_confirmed = models.BooleanField(default=False)
    user_phone = models.IntegerField(default=0)
    discounted_price = models.IntegerField(default=0)

    def get_total_cart_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_item_total_price()
        return total

    def get_total_discount_price(self):
        disc_total = 0
        for item in self.items.all():
            disc_total += item.get_item_discount_price()
        return disc_total

    #@admin.display(ordering = 'order_date',description = "new orders")
    def get_new_orders(self):
        return self.items.filter(agent_confirmed=False)

    def __str__(self):
        return str(self.ref_code)
