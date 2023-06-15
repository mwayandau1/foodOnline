from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from menu.models import Category, FoodItem
from .models import Cart
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count' : vendor_count,
    }
    return render(request,'marketplace/listings.html', context )

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('fooditems', queryset=FoodItem.objects.filter(is_available=True))
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories' : categories,
        'cart_items':cart_items
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if food item exist
            try:
                food_item = FoodItem.objects.get(id=food_id)
                #check if the user has already added same  food item
                try:
                    cart = Cart.objects.get(user=request.user, food_item=food_item)
                    cart.quantity += 1
                    cart.save()
                    return JsonResponse({'status': 'success', 'message': 'Cart quantity increased'})
                except:
                    cart = Cart.objects.create(user=request.user, food_item=food_item, quantity=1)
                    return JsonResponse({'status': 'success', 'message': 'Cart created successfully'})
            except:
                return JsonResponse({'status':'failed', 'message': 'Food Item does not exist'})
        else:

            return JsonResponse({'status': 'failed', 'message': 'Invalid Request'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Please login to continue'})
