from django.shortcuts import render,redirect
from ecom_auth.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from math import ceil
import razorpay
from django.conf import settings
# from ecom_apk import keys
# MERCHANT_KEY = keys.MK
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum
from django.core.exceptions import ValidationError
# from ecom_apk.keys import MID, MK

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def index(request):
    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds}
    return render(request,'index.html',params)




def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        pnumber=request.POST.get('phonenumber')
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request, 'We will get back soon as possible')
        return render(request,"contact.html")
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to checkout")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt', '')
        print(amount, "amount")
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        size=request.POST.get('size','')
        # amount = "100"
        Order = Orders(items_json=items_json, name=name, email=email,size=size, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True

        currency = 'INR'

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=int(amount) * 100,
                                                        currency=currency,
                                                        payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = ''

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url


        return render(request, 'paytm.html', context)

    return render(request, 'checkout.html')

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
          
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'paymentstatus.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'activatefail.html')
            else:

                # if signature verification fails.
                return render(request, 'activatefail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest("Page is errors")
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest("page is errors")
    



# def profile(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "Please login to checkout")
#         return redirect('/auth/login')
    
#     currentuser = request.user.username
#     items = Orders.objects.filter(email=currentuser)
#     rid=""
    
#     for i in items:
#         print(i.oid)  
#         # print(i.order_id)
#         myid = i.oid
#         rid = myid.replace("ZKcart", "")
#         print(rid)

#     # status=OrderUpdate.objects.filter(order_id=int(rid))
#     # print(status)
    
#     context = {'items': items}  
#     # ,"status":status
#     print(currentuser)
    
#     return render(request, 'profile.html', context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view your profile.")
        return redirect('/auth/login')

    currentuser = request.user.email  # Adjust to username if necessary
    items = Orders.objects.filter(email=currentuser)
    
    # Attach delivery status from OrderUpdate
    orders_with_updates = []
    for order in items:
        order_updates = OrderUpdate.objects.filter(order_id=order.order_id).first()
        orders_with_updates.append({
            'order': order,
            'delivery_status': order_updates.deliverd if order_updates else "Pending"
        })

    context = {'orders_with_updates': orders_with_updates}
    return render(request, 'profile.html', context)

    