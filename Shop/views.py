from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404
from .models import Item,CartItem,Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import Http404
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView,DetailView,CreateView,DeleteView
from .forms import checkoutform,promocodeform
from payment.code_generator import refcode
from USERS.models import PromoCode,profile

class homeview(ListView):
    model = Item
    template_name = 'Shop/home-page.html'
    context_object_name = 'products'
    paginate_by=4

@login_required
def productview(request,product_id):
    try:
        product = get_object_or_404(Item,pk=product_id)
    except Http404 :
        return redirect('Shop:home')
    #product= Item.objects.get(pk=product_id)
    cart,created = Cart.objects.get_or_create(owner=request.user,ordered=False)
    items = cart.items.filter(user=request.user,ordered=False)
    try:
        related_items = Item.objects.filter(category=product.category)[:3]
    except Http404:
        related_items=Item.objects.all()[:3]
    total = items.count()
    #print(request.headers)

    return render(request,'Shop/product-page.html',{"related_items":related_items,"product":product,"cart_total":total})

@login_required
def checkoutview(request):
    try:
        cart = get_list_or_404(Cart,owner=request.user,ordered=False)[0]
    except Http404 :
        return redirect('Shop:home')
    items = cart.items.filter(user=request.user,ordered=False)
    total = items.count()
    form = checkoutform()
    pform = promocodeform()
    if request.method == "POST":
        form = checkoutform(request.POST)
        if form.is_valid(): #DO custom validations
            cart.street_name = form.cleaned_data['street_name']
            cart.county = form.cleaned_data['sub_county']
            cart.location = form.cleaned_data['ward']
            payment = form.cleaned_data['payment_options']
            cart.order_date = timezone.now()
            cart.user_phone = request.user.profile.cell_number#error handling incase user has no cell number
            cart.payment_method = payment
            if cart.discounted_price:
                cart.total_price = cart.discounted_price
            else:
                cart.total_price = cart.get_total_cart_price()
            for item in items: # this here loops through the carts items making them ordered=true
                item.ordered = True
                item.save()
            cart.ref_code = refcode()
            cart.ordered = True
            cart.save()
            if payment == 'LipanaMpesa':
                return HttpResponseRedirect(reverse('index'))
            #cart.user_phone = request.user.username
            return redirect('Shop:order-success')# redirect to a succes page whih will tell the user to wait for agent confirmation call

        return redirect('Shop:checkout')
    context= {
        "items":items,
        "cart_total":total,
        "cart":cart,
        "form":form,
        "pform":pform

    }

    return render(request,'Shop/checkout-page.html',context)

@login_required
def redeem(request):
    try:
        cart = get_list_or_404(Cart,owner=request.user,ordered=False)[0]
    except Http404 :
        return redirect('Shop:home')
    items = cart.items.filter(user=request.user,ordered=False)
    total = items.count()
    form = checkoutform()
    discount= 0

    if request.method == 'POST':
        pform = promocodeform(request.POST)
        if pform.is_valid:
            promocode = pform.cleaned_data['p_code']
            try:
                code = get_object_or_404(PromoCode,token=promocode)
            except Http404:
                code ="invalid"
                messages.warning(request,'invalid promocode, please input the correct/updated agent refcode !')
                return redirect('Shop:checkout')
            agent = code.owner.commission
            discount = cart.get_total_discount_price()//2
            cart.discounted_price = cart.get_total_cart_price()-discount
            cart.agent_code = promocode
            agent += discount
            cart.save()
            print('discount',discount,'comm',agent,cart.discounted_price)

    context= {
        "items":items,
        "cart_total":total,
        "cart":cart,
        "form":form,
        "pform":pform,
        "promocode":promocode,
        "discount":discount

    }

    return render(request,'Shop/checkout-page.html',context)


@login_required
def ordersummary(request):
    try:
        cart = get_list_or_404(Cart,owner=request.user,ordered=False)[0]
    except Http404 :
        return redirect('Shop:home')

    items = cart.items.filter(user=request.user,ordered=False)
    if cart and items.exists():
        context= {
            "items":items,
            "cart":cart
        }

        return render(request,'Shop/order-summary.html',context)
    else:
        messages.info(request,'you have no active order')
        return redirect('Shop:home')

@login_required
def ordersuccess(request):
    try:
        qs = get_list_or_404(Cart,owner=request.user,ordered=True)
    except Http404 :
        return redirect('Shop:home')
    #qs = Cart.objects.filter(owner=request.user,ordered=True)
    last = len(qs)-1
    cart = Cart.objects.filter(owner=request.user,ordered=True)[last]
    ref= cart.ref_code
    return render(request,'Shop/order-success.html',{"refcode":ref})

class categoryview(ListView):
    model = Item
    template_name = 'Shop/category-page.html'
    context_object_name = 'products'
    paginate_by= 4

    def get_queryset(self):
        return Item.objects.filter(category=self.kwargs.get('category'))

@login_required
def add_to_cart(request,product_id):
    try:
        product = get_object_or_404(Item,pk=product_id,in_stock=True)
    except Http404 :
        return redirect('Shop:home')
    #product = Item.objects.get(pk=product_id)
    if request.user.is_authenticated:
        #get the info from the user and make a cart_item the look if the user has an existing cart so get or create
        cart_item,created=CartItem.objects.get_or_create(user=request.user,item=product,ordered=False)

        # check if the user has an existing order which is not purchased
        query=Cart.objects.filter(owner=request.user,ordered = False)
        if query.exists():
            cart = query[0]

            #check if the order exists in the cart---ts y you look at the cart.items not cart
            if cart.items.filter(item=product):
                print('in the cart')
                cart_item.quantity +=1
                cart_item.save()
                messages.info(request,f'{cart_item.item.title} quantity has been updated in your cart')
            else:
                cart.items.add(cart_item)
                messages.info(request,f'{cart_item.item.title} has been added to your cart')
        else: # if the user has no cart make one with date and user and ordered = false the add the cart item we made
            print('created a new cart')
            new_cart = Cart.objects.create(
                owner=request.user,
                ordered=False,
                order_date=timezone.now()
            )
            new_cart.items.add(cart_item)

        return redirect('Shop:order-summary')
    else:
        return redirect('users:login')

@login_required
def remove_from_cart(request,product_id):
    try:
        product = get_object_or_404(Item,pk=product_id)
    except Http404 :
        return redirect('Shop:home')
    #product = Item.objects.get(pk=product_id)
    if request.user.is_authenticated:
        # check if the user has an existing order which is not purchased
        query=Cart.objects.filter(owner=request.user,ordered = False)
        if query.exists():
            cart = query[0]
            if request.user == cart.owner:
            #check if the item to remove exists in the cart get the cart item then remove it
                if cart.items.filter(item=product):
                    cart_item = CartItem.objects.filter(user=request.user,item=product,ordered=False)[0]
                    cart.items.remove(cart_item)
                    messages.info(request,f'{cart_item.item.title} has been removed from your cart')

                else:
                    messages.info(request,'this item is not in your cart')

        else:
            messages.info(request,'You have not placed any order yet')

        return redirect('Shop:order-summary')
    else:
        messages.warning('log in or create account first to shop')
        return redirect('users:login')

@login_required
def remove_singleitem_from_cart(request,product_id):
    try:
        product = get_object_or_404(Item,pk=product_id)
    except Http404 :
        return redirect('Shop:home')
    #product = Item.objects.get(pk=product_id)
    if request.user.is_authenticated:
        # check if the user has an existing order which is not purchased
        query=Cart.objects.filter(owner=request.user,ordered = False)
        if query.exists():
            cart = query[0]
            if request.user == cart.owner:
            #check if the item to remove exists in the cart get the cart item then remove it
                if cart.items.filter(item=product):
                    cart_item = CartItem.objects.filter(user=request.user,item=product,ordered=False)[0]
                    if cart_item.quantity > 1:
                        cart_item.quantity -=1
                        cart_item.save()
                        messages.info(request,f'{cart_item.item.title} quantity has been decreased from your cart')
                    else:
                        cart.items.remove(cart_item)
                        messages.info(request,f'{cart_item.item.title} has been removed from your cart')

                else:
                    messages.info(request,f'{cart_item.item.title} is not in your cart')

                    #display message
            #log user ip
        else:
            messages.info(request,'You have not placed any order yet')

        return redirect('Shop:order-summary')
    else:
        messages.warning('log in or create account first to shop')
        return redirect('Shop:order-summary')
