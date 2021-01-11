def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          # get_or_create --> tiene la ventaja de ser dos en uno
          #primero trata de buscar el objeto y si no lo encuentra
          # crea uno nuevo
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          #order es padre y orderitem es hijo
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          #Esto es para pasar las cookies a la vista de django
          # Pero hay que hacerles parsing con json
          #dentro de un try, por que la primera vez no vas
          #a tener Cart.
          try:
               cart = json.loads(request.COOKIES['cart'])
          except:
               cart = {}
          print('Cart:', cart)
          items = []
          order = {'get_cart_total':0,'get_cart_items':0, 'shipping': False}
          cartItems = order['get_cart_items']
          #Para pasar por un bucle el carrito de compra (cart)
          #incrementa cartitems en cada iteracion
          # y así incrementar el carrito que ves en rojo a la
          #derecha
          for i in cart:
               try:
                    cartItems += cart[i]["quantity"]
                    product = Product.objects.get(id=i)
                    total = (product.price * cart[i]["quantity"])

                   order['get_cart_total'] += total
                   order['get_cart_items'] += cart[i]["quantity"]
                   #el siguiente cod es el que va a mostrar
                   #las imagenes y demas datos en el Cart
                   #los nombre de los atributos de product
                   #deben corresponder, si no da error
                   item = {'product':{
                    'id':product.id, 
                    'name':product.name,
                    'price':product.price,
                    'image_url': product.image_url,     
                    },
                       'quantity':cart[i]['quantity'],
                       'get_total':total,
                       }
                   items.append(item)

                   if product.digital == False:
                        order['shipping'] = True

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context
