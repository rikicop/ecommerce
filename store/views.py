from django.shortcuts import render
#from django.shortcuts import HttpResponse
#import pandas as pd
import json
import datetime
from django.http import JsonResponse

from .models import *
from .utils import cookieCart,cartData,guestOrder
# Create your views here.
def store(request):
     
     data = cartData(request)
     cartItems = data['cartItems']
     
     products=Product.objects.all()
     context = {'products':products, 'cartItems':cartItems}
     return render(request, 'store/store.html', context)

def cart(request):
     
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body.decode('utf-8'))
     productId = data['productId']
     action = data['action']
     print('Action:', action)
     print('ProductId:',  productId)

     customer = request.user.customer
     product=Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

     if action == 'add':
          orderItem.quantity =  (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity =  (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('Item was added', safe=False)

def processOrder(request):
     product=Product.objects.get(name='zapatos')
     transaction_id = datetime.datetime.now().timestamp()
     # Esto es necesarion para tomar después el
     # formulario del Body
     data = json.loads(request.body.decode('utf-8'))

     if request.user.is_authenticated:
          customer = request.user.customer
          order , created =  Order.objects.get_or_create(customer = customer , complete=False)
          #Acuerdate que obtienes este form gracias
          #al json.loads(request.body)
         
     else:
          customer, order = guestOrder(request,data)
          print('***Hola soy processOrder y Corrí correctamente**')
          print('product stock de zapatos:',  product.stock )
          cart_cookie  = request.COOKIES['cart']
          cart_json = json.loads(cart_cookie)
          print('El carrito: ', cart_json)

          
     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if  total == float(order.get_cart_total):
          order.complete = True
     order.save()

     
     if order.shipping == True:
          ShippingAddress.objects.create(
               customer = customer,
               order = order,
               address = data['shipping']['address'],
               city = data['shipping']['city'],
               state = data['shipping']['state'],
               zipcode = data['shipping']['zipcode'],
          )
     
     return JsonResponse('Payment complete!', safe=False)

      


#Esto no es del ecommerceoriginal
# Creo que esto era para hacer una tabla bonita
#Te falta el archivo de la oms que tienes en
#DjangoProjects

#def looper_view(request):
#	df= pd.read_csv("static/csv/oms.csv")

	#parse to json
	#json_records = df.reset_index().to_json(orient ='records')
	#data = []
	#data = json.loads(json_records)
	#context = {'d': data}
	#print(context)
	#return render(request, 'store/looper.html', context)
