from django.contrib import admin
from marketplace.models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'date_modified')  # Fixed typo: 'food_item' instead of 'food_tem'

admin.site.register(Cart, CartAdmin)
