from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from django.contrib import messages

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()
            # messages.success(request, 'account registered successfully')
            # return redirect('registerUser')

            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(f_name, l_name, username, email, password)
            user.role = User.VENDOR
            user.save()
            messages.success(request, 'account registered successfully')
            return redirect('registerUser')
    else:
        form = UserForm
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context )


def registerVendor(request):
    if request.method == "POST":
        #store the data and creater user
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(f_name=f_name, l_name=l_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            print(user_profile)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your account has been registered successfully. Please wait for approval")
            return redirect('registerVendor')
    else:

        form = UserForm()
        vendor_form = VendorForm()
    context = {
        'form':UserForm,
        'vendor_form':VendorForm
    }
    return render(request, 'accounts/registerVendor.html', context)
