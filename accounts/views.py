from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from .utils import detectUser, send_email_verification
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages, auth
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
#Restrict vendor from accessing customer page


def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict customer from accessing vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
      raise  PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('myAccount')
    elif request.method == 'POST':
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
            user.role = User.CUSTOMER
            user.save()
            # Send verifaction email
            mail_subject = "Please acitvate your account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_email_verification(request, user, mail_subject, email_template)

            messages.success(request, 'account registered successfully')
            return redirect('registerUser')
    else:
        form = UserForm
    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context )


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('myAccount')
    elif request.method == "POST":
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
            vendor.user_profile = user_profile
            vendor.save()
            #Send verifaction email
            mail_subject = "Please acitvate your account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_email_verification(request, user, mail_subject, email_template)
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


def activate(request, uidb64, token):
    # Activate the user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account has been activated")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid Activation Link")
        return redirect('myAccount')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('myAccount')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, "Invalid Password or Email")
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def cusDashboard(request):
    return render(request, 'accounts/cusDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def venDashboard(request):
    vendor = Vendor.objects.get(user=request.user)

    return render(request, 'accounts/venDashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email =request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            #Send the password reset link

            mail_subject = "Please reset your password!"
            email_template = "accounts/emails/send_password_reset_email.html"
            send_email_verification(request, user, mail_subject, email_template)
            messages.success(request, "Password reset link has been sent to your email account")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request,  uidb64, token):
    #Validate the the use by decoding the token
    # Activate the user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, "Please activate your account")
        return redirect('reset_password')
    else:
        messages.error(request, "This link has expired!")
        return redirect('myAccount')



def reset_password(request):
    if request.method == 'POST':
       password = request.POST['password']
       confirm_password = request.POST['confirm_password']
       if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password set successfully!")
            return redirect('login')
       else:
           messages.info(request, "Password do not match")
    return render(request, 'accounts/reset_password.html')
