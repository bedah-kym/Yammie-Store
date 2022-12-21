from django.contrib.auth.decorators import login_required
from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient
from .forms import payment_form
from Shop.models import Cart
from .models import payment_info
from USERS.models import profile
from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect,render,get_object_or_404

@login_required
def index(request):
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
            #payment_info.objects.create(phone_number=phone_number,amount=amount,cart_number=cart,user=request.user)#create if response is +ve
            account_reference = 'yammie feeds'
            transaction_desc = f'Pay yammie feeds for online order number{cart.ref_code}'
            callback_url= 'https://darajambili.com'
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            return HttpResponse(response)
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
        else:
            return redirect('chargeclient')

    return render(request,'payment/payment_form.html',{"form":form})


@login_required
def payagent(request):
    """find the profile of the request owner,check if user is an agent, check the amount if conditions meet then can withdraw else
        no withdrawal.
    """
    form=payment_form(request.POST)
    ans=False
    try:
        userprofile = get_object_or_404(profile,user_name=request.user)
        if userprofile.is_sales_agent == True or userprofile.is_anon_agent == True:
            agentprofile=userprofile
        else:
            raise Http404
    except Http404 :
        return redirect ('users:profile')
    if request.method == "POST":
        form=payment_form(request.POST)
        if form.is_valid:
            cl = MpesaClient()
            if agentprofile.commission < 200:
                ans=agentprofile.commission
                phone_number = str(agentprofile.cell_number)
                amount = ans
                transaction_desc = f'anon agent {agentprofile.user_name} paid. '
                occassion = 'commission'
                callback_url = 'https://darajambili.com'
                response = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)


    return render(request,'payment/temp.html',{'form':form,'ans':ans})
