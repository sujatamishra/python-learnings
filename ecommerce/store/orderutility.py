import json
from .models import *


def cookieCart(request):
    try:
            cart=json.loads(request.COOKIES['cart'])
    except:
            cart={}    
          
    print("cart== ",cart)
    items=[]
    order={'get_cart_items':0,'get_cart_total':0,"shipping":False}  
    cartItems= order['get_cart_items']

    for i in cart:
        try: 
            cartItems+=cart[i]['quantity']
            product=Product.objects.get(id=i)
            total=(product.price*cart[i]["quantity"])
            order['get_cart_total']+=total
            order['get_cart_items']+=cart[i]["quantity"]

            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                    },
                    'quantity':cart[i]["quantity"],
                    'get_total':total
                }

            items.append(item)
            print("items===== ",items)

            if product.digital == False:
                order['shipping']=True
        except:
            pass 
    return {"cartItems":cartItems,"items":items,"order":order}

def cartData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        cookieData=cookieCart(request)
        items=cookieData['items']
        order=cookieData['order']
        cartItems=cookieData['cartItems']

    return {"items":items,"order":order,"cartItems":cartItems}      

def guestOrder(data,request):
    name=data['userFormData']['name']
    email=data['userFormData']['email']
    cookieData=cookieCart(request)
    items=cookieData['items']
    customer,created=Customer.objects.get_or_create(email=email,)
    customer.name=name
    customer.save()
    order=Order.objects.create(customer=customer,complete=False)

    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItem=OrderItem.objects.create(order=order,product=product,quantity=item['quantity'])

    return order,customer        
