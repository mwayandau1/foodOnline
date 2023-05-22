from django import forms
from .models import User
from accounts.models import UserProfile
from .validators import allow_only_image_validator
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['f_name', 'l_name', 'username', 'email','password']


def clean(self):
    clean_data = super(UserForm, self).clean()
    password = clean_data.get('password')
    confirm_password = clean_data.get('confirm_password')
    if password != confirm_password:
        raise forms.ValidationError("Password do not match each other")


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'} ), validators=[allow_only_image_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}), validators=[allow_only_image_validator])
    #First way of making it read only
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))


    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    #Second way to make it read only
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
