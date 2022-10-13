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
    """
        assisted by the django-daraja package this function gets all the ordered carts a user has and gets the last ordered cart
        then input from the form is passed along other variables from the selected cart. this variables will create a
        new instace of payment_info.

        after creating a new instance django_daraja pushes an stk push to safaricom which returns a json response,
        if successfull the agent_code in the cart links back to the Agents profile and adds the commission earned to the
        agent.
    """

    form=payment_form()
    qs = Cart.objects.filter(owner=request.user,ordered=True)
    last = len(qs)-1
    cart = Cart.objects.filter(owner=request.user,ordered=True)[last]
    if request.method =="POST":
        form=payment_form(request.POST)
        if form.is_valid():
            cl = MpesaClient()
            phone_number = form.cleaned_data['phone_number']
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
            #pays the agent commission earned if transaction is successfull
            promocode = cart.agent_code
            try:
                qs = PromoCode.objects.get(token=promocode)
                profile = qs.owner
                discount = cart.get_total_discount_price()//2
                profile.commission += discount
                profile.save()
                print('commission paid :',profile.commission)
            except Http404 :
                cart.ordered = False
                return redirect('Shop:checkout')

            return HttpResponse(response,'Shop/order-succes.html') #redirect to the success page

    return render(request,'Shop/payment_form.html',{"form":form,})
