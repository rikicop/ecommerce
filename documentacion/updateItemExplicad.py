

def updateItem(request):
     data = json.loads(request.body.decode('utf-8'))
     productId = data['productId']
     action = data['action']
     print('Action:', action)
     print('ProductId:',  productId



<div class="box-element product">
      <h6><strong>{{product.name}}</strong></h6>
      <hr>
      <button data-product={{product.id}} data-action="add"
       class="btn btn-outline-secondary add-btn update-cart">
	  Add to Cart
       </button>
      <a class="btn btn-outline-success" href="#">View</a>
      <h4 style="display: inline-block; float: right">
	<strong>${{ product.price|floatformat:2  }}</strong>
      </h4>
</div>
