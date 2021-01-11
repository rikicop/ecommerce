//Primero vamos a obtener todos los botones
var updateBtns = document.getElementsByClassName('update-cart')

//con this.dataset es que acedemos a los atributos de html
// Con respecto al user , lo obtiene del script que hiciste en la cabecera
// de main.html var user = '{{ request.user  }}'
for(var i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
	var productId = this.dataset.product
       var action = this.dataset.action
	console.log('productId', productId, 'action:',action )

	console.log('USUARIO:', user)
	if(user === 'AnonymousUser'){
	    addCookieItem(productId,action)
	}else{
	    updateUserOrder(productId,action)
	}
	
    })
}

function  addCookieItem(productId, action){
    console.log('User no está logeado...')
    if (action == 'add') {
	if(cart[productId] == undefined){
	    cart[productId] = {'quantity' : 1}
	}else {
	    cart[productId]['quantity'] += 1
	}
    }
	if (action == 'remove'){
	    cart[productId]['quantity'] -= 1
	    if(cart[productId]['quantity'] <= 0){
		console.log('Remove Item')
		delete cart[productId]
	    }
	}
    console.log('Cart:', cart)
    document.cookie = 'cart='  +  JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


function updateUserOrder(productId, action){

    console.log('User si esta logeado, enviando data...')

    var url = '/update_item/'
    //body son los datos que envio al backend
    // Para X-CSRFToken': csrftoken, tienes que habilitar una función en
    //En el script del </header> de  main.html llamada:  function getToken()
    fetch(url,{
	method:'POST',
	headers:{
	    'Content-Type':'application/json',
	    'X-CSRFToken': csrftoken,
	},
	body:JSON.stringify({'productId': productId, 'action': action})
    })
	.then((response)=>{
	    return response.json()
	})
        .then((data)=>{
            console.log('data:', data)
	    location.reload()
	})
}
