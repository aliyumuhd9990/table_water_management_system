from .models import *
from .views import _CartId

# cart/context_processors.py

def cart_counter(request):
    count = 0
    if request.user.is_authenticated:
        try:
            # cart = Cart.objects.get(user=request.user)
            count = CartItem.objects.filter(user=request.user).count()
        except Cart.DoesNotExist:
            count = 0
    else:
        # For anonymous users (if you're using session cart)
        # cart_id = request.session.get('cart_id')
        cart_id = Cart.objects.filter(cart_id=_CartId(request)).count()
        if cart_id:
            count = CartItem.objects.filter(cart=cart_id).count()

    return {'cart_count': count}
