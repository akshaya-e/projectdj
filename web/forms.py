from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Package



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','role','email','password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    pass 

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['title', 'destination',  'price','image','duration','description','expiry_date']
    expiry_date=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    


class VendorRegistrationForm(UserCreationForm):
    company_name=forms.CharField(max_length=100,required=True,label="Company name")
    contact_number=forms.CharField(max_length=50,required=True,label="Contact number")
    address=forms.CharField(widget=forms.Textarea,required=True,label="Address")
    
    class Meta:
        model=CustomUser
        fields=['username','email','password1','password2']
    
    def save(self,commit=True):
        from .models import Vendor
        user=super().save(commit=False)
        user.role='vendor'
        if commit:
            user.save()
            Vendor.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                contact_number=self.cleaned_data['contact_number'],
                address=self.cleaned_data['address'],
            )
            return user

