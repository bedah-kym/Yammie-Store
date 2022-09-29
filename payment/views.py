from django.contrib.auth.decorators import login_required
from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient
from .forms import payment_form
from Shop.models import Cart
from .models import payment_info

@login_required
def index (request):
    form=payment_form()
    qs = Cart.objects.filter(owner=request.user,ordered=True)
    last = len(qs)-1
    cart = Cart.objects.filter(owner=request.user,ordered=True)[last]
    if request.method =="POST":
        form=payment_form(request.POST)
        if form.is_valid():
            cl = MpesaClient()

            phone_number = request.POST.get('phone_number')
            amount = cart.total_price
            payment = cart.payment_method
            user = cart.owner
            street = cart.street_name
            Location = cart.location
            County = cart.county

            payment_info.objects.create(phone_number=phone_number,amount=amount,cart_number=cart,user=request.user)
            account_reference = 'yammie feeds'
            transaction_desc = f'Pay yammie feeds for online order number{cart.ref_code}'
            callback_url='https://darajambili.herokuapp.com/c2b/confirmation'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            return HttpResponse(response) #redirect to the success page

    return render(request,'Shop/payment_form.html',{"form":form,})


def index2(request):
    cl = MpesaClient()
    #token = cl.access_token()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0748677515'
    amount = 10
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url='https://darajambili.herokuapp.com/c2b/confirmation'
    #callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)
