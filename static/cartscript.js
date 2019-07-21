/* Set rates + misc */
var taxRate = 0.05;
var shippingRate = 15.00;
var fadeTime = 300;
var features=[];
features.push({"item":"Dingo Dog Bones","description":"The best dog bones of all time. Holy crap. Your dog will be begging for these things! I got curious once and ate one myself. I`m a fan.","img":'https://s.cdpn.io/3/dingo-dog-bones.jpg',"price":12.99});
features.push({"item":"Nutro™ Adult Lamb and Rice Dog Food","description":"Who doesn't like lamb and rice? We've all hit the halal cart at 3am while quasi-blackout after a night of binge drinking in Manhattan. Now it`s your dog`s turn!","img":"https://s.cdpn.io/3/large-NutroNaturalChoiceAdultLambMealandRiceDryDogFood.png","price":45.99});


/* Assign actions */
$('.product-quantity input').change( function() {
  updateQuantity(this);
});

$('.product-removal button').click( function() {
  removeItem(this);
});
function addProduct(id){
  addtoCart(features[id]);
}
// $('.add-product').click(function(){
//   //alert('called add..');
//   addtoCart(features[parseInt($('#addSelect').val())]);
// });
function addtoCart(feature){
  $('.column-labels').after('<div class="product"><div class="product-image"><img src="'+feature.img+'"></div><div class="product-details"><div class="product-title">'+feature.item+'</div><p class="product-description">'+feature.description+'</p></div><div class="product-price">'+feature.price+'</div><div class="product-quantity"><input type="number" value="1" min="1"></div><div class="product-removal"><button class="remove-product">Remove</button></div><div class="product-line-price">'+feature.price+'</div></div>');
  $('.product-removal button').unbind();
  $('.product-quantity button').unbind();
  $('.product-removal button').click( function() {
  removeItem(this);
  });
  $('.product-quantity input').change( function() {
  updateQuantity(this);
});
  recalculateCart();
}
/* Recalculate cart */
function recalculateCart()
{
  var subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });

  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal + tax + shipping;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal.toFixed(2));
    $('#cart-tax').html(tax.toFixed(2));
    $('#cart-shipping').html(shipping.toFixed(2));
    $('#cart-total').html(total.toFixed(2));
    if(total == 0){
      $('.checkout').fadeOut(fadeTime);
    }else{
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });


}

/* Update quantity */
function updateQuantity(quantityInput)
{
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.product-price').text());
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toFixed(2));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });
}


/* Remove item from cart */
function removeItem(removeButton)
{
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
  });
}
