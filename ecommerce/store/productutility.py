from django.shortcuts import render
from .models import *
from tablib import Dataset
from django.contrib import messages

def addProductsData(request):
    try:
          print("try block")
          if request.method == 'POST':
               flag=False  
               dataset = Dataset()
               productsData = request.FILES['myfile']
               
               if not productsData.name.endswith('xlsx'):
                    messages.info(request,'wrong format')
                    return render(request, 'store/addProducts.html')

               imported_data = dataset.load(productsData.read(),format='xlsx')
               #print("imported_data========= ",imported_data)
               
               objs=[]
               print("len(objs)===== ",len(objs))
               fixedCount=10
               count=0
               for data in imported_data:
                    product=Product.objects.filter(name=data[0])
                    #print("product****== ",product)

                    if not product:
                         objs.append(Product(name=data[0],price=data[1],digital=data[2],image=data[3]))
                         #print("objs55===",objs)
                         #print("product=== ",product)
                         count += 1
                         #print("count== ",count)
                         
                         if count == fixedCount:
                              print("objs#####= ",objs)
                              product = Product.objects.bulk_create(objs=objs)
                              print("product**********===========  ",product)
                              objs=[]
                              count=0
                              flag=True 
                    #else:    
                         #print("product22****== ",product)
               if objs:
                    print("objs111=== ",objs)
                    #print("type of objs=== ",type(objs))
                    for i in objs:
                         #print("i111=== ",type(i))
                         #print("i111=== ",i.name)
                         if i.name is None:
                              print("i1112=== ",i)
                              objs.remove(i)
                    if objs:          
                         product = Product.objects.bulk_create(objs=objs)
                         print("product3333==== ",product)
                         flag=True 

               if flag == False:
                         messages.info(request,'All records of given data already exist')  
          
    except Exception as e:
          print("Exception=== ",e)
          messages.info(request,"exception is "+str(e))