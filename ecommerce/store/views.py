from django.shortcuts import render
from .models import *
from .orderutility import *
from .productutility import *
from django.http import JsonResponse
import json
import datetime
from tablib import Dataset
from django.contrib import messages
from .filters import ProductFilter




# Create your views here.
def store(request):
     data=cartData(request)
     cartItems=data['cartItems']
     products=Product.objects.order_by('-id')
     myFilter=ProductFilter(request.GET,queryset=products)
     products=myFilter.qs
     context = {"productsData":products,"cartItems":cartItems,'myFilter':myFilter}
     return render(request, 'store/store.html', context)

def cart(request):
     data=cartData(request)
     items=data['items']
     order=data['order']
     cartItems=data['cartItems']

     context = {"items":items,"order":order,"cartItems":cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     data=cartData(request)
     items=data['items']
     order=data['order']
     cartItems=data['cartItems']
     context = {"items":items,"order":order,"cartItems":cartItems}
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data=json.loads(request.body)
     productId=data['productId']
     action=data['action']
     print("productId== ",productId)
     print("action== ",action)
     customer=request.user.customer
     product=Product.objects.get(id=productId)
     order,created=Order.objects.get_or_create(customer=customer,complete=False)
     orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

     if action == "add":
          orderItem.quantity=(orderItem.quantity+1)
          msg="Item was added"
     elif action == "remove":
          orderItem.quantity=(orderItem.quantity-1)
          msg="Item was removed"

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse(msg,safe=False)  

def processOrder(request):
     print("request.body===== ",request.body)
     data=json.loads(request.body)
     transaction_id=datetime.datetime.now().timestamp()
     print("transaction_id=======",transaction_id)
     if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)

     else:
        print("user not logged in")
        order,customer=guestOrder(data,request)
     total=float(data['userFormData']['total'])
     order.transction_id=transaction_id 

     if total == order.get_cart_total:
          order.complete=True 
     order.save()

     if order.shipping == True:
          ShippingAddress.objects.create(customer=customer,order=order,
          address=data['shippingInfo']['address'],
          city=data['shippingInfo']['city'],
          state=data['shippingInfo']['state'],
          zipcode=data['shippingInfo']['zipcode'],
          )
            
     return JsonResponse("Payment complete",safe=False)

  
def addProducts(request):
     addProductsData(request)
     context={"msg":"success"}
     return render(request, 'store/addProducts.html', context)