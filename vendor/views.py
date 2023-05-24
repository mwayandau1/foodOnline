from django.shortcuts import render, get_object_or_404, redirect
from vendor.forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
from menu.forms import FoodItemForm


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def ven_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "Changes Updated Successfully")
            return redirect('ven_profile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/ven_profile.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    category = Category.objects.filter(vendor=vendor).order_by('-date_created')
    context = {

        'category':category,
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor =get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems': fooditems,
        'category':category,
    }
    return render(request, 'vendor/fooditems_by_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            category_name = forms.cleaned_data['category_name']
            category = forms.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            forms.save()
            messages.success(request, "Category Added Successfully")
            return redirect('menu_builder')
    else:
        forms = CategoryForm()
    context = {
        'forms': forms
    }
    return render(request, "vendor/add_category.html", context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,  pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        forms = CategoryForm(request.POST, instance=category)
        if forms.is_valid():
            category_name = forms.cleaned_data['category_name']
            category = forms.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            forms.save()
            messages.success(request, "Category Modified Successfully")
            return redirect('menu_builder')
    else:
        forms = CategoryForm(instance=category)
    context = {
        'forms': forms,
        'category':category,
    }

    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,  pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category Deleted Successfully!')
    return redirect('menu_builder')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        forms = FoodItemForm(request.POST, request.FILES)
        if forms.is_valid():
            food_tile = forms.cleaned_data['food_title']
            food = forms.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_tile)
            forms.save()
            messages.success(request, "Food Item Added Successfully")
            return redirect('fooditems_by_category', food.category.id)
    else:
        forms = FoodItemForm()
        forms.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'forms': forms
    }
    return render(request, 'vendor/add_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,  pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        forms = FoodItemForm(request.POST, instance=food)
        if forms.is_valid():
            food_title = forms.cleaned_data['food_title']
            food = forms.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            forms.save()
            messages.success(request, "Food Item Modified Successfully")
            return redirect('fooditems_by_category', food.category.id)
    else:
        forms = FoodItemForm(instance=food)
        forms.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'forms': forms,
        'food' : food,
    }

    return render(request, 'vendor/edit_food.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request,  pk):
    food = get_object_or_404(FoodItem, pk=pk)
    food.delete()
    messages.success(request, 'Food Item Deleted Successfully!')
    return redirect('fooditems_by_category', food.category.id)