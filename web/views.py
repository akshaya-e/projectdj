from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PackageForm,VendorRegistrationForm
from .models import CustomUser,Package, Booking,User
from celery import shared_task
from django.utils import timezone
from web.models import Package

# Create your views here.

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method=='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form=CustomUserCreationForm()
    return render(request,'register.html',{'form': form})


def vendor_register(request):
    if request.method=='POST':
        form=VendorRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            return redirect('login')
    else:
        form=VendorRegistrationForm()
    return render(request,'vendor_register.html',{'form':form})
        



def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_packages')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')




def list_packages(request):
        available_packages = Package.objects.filter(approved=True)
        return render(request, 'package_list.html', {'packages': available_packages})
   


# Vendor Create a new package
@login_required
def create_package(request):
    if request.user.role != 'vendor':
        return redirect('home')

    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            package.vendor = request.user
            package.save()
            return redirect('list_packages')
    else:
        form = PackageForm()
    return render(request, 'create_package.html', {'form': form})

# Display only approved packages to users
def list_packages(request):
    packages = Package.objects.filter(approved=True)
    return render(request, 'package_list.html', {'packages': packages})

# Book a package
@login_required
def book_package(request, package_id):
    package = get_object_or_404(Package, id=package_id, approved=True)
    if request.method == 'POST':
        booking = Booking.objects.create(user=request.user, package=package)
        booking=Booking(user=request.user,package=package)
        booking.save()
        #booking.status = "Completed"
        #booking.save()
        #messages.success(request, 'Package booked successfully. Payment pending.')
        return redirect('list_packages')
    return render(request, 'book_package.html', {'package': package})

# Admin only Approve packages
@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def approve_package(request, package_id):
    package = get_object_or_404(Package, id=package_id, approved=False)
    package.approved = True
    package.save()
    return redirect('pending_packages')

# Admin only View pending packages
@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def pending_packages(request):
    packages = Package.objects.filter(approved=False)
    return render(request, 'pending_packages.html', {'packages': packages})


@shared_task
def delete_expired_packages():
    deleted_count,_ = Package.objects.filter(expiry_date__lt=timezone.now()).delete()
    return f"Deleted {deleted_count} expired packages"
    
    

@login_required
def edit_package(request,package_id):
    package=get_object_or_404(Package, id=package_id)
    if request.method=='POST':
        form=PackageForm(request.POST,request.FILES,instance=package)
        if form.is_valid():
            form.save()
            return redirect('list_packages')
    else:
        form=PackageForm(instance=package)
    return render(request,'edit_package.html',{'form':form})

@login_required
def delete_package(request,package_id):
    package=get_object_or_404(Package,id=package_id)
    if request.method=='POST':
        package.delete()
        return redirect('list_packages')
    return render(request,'delete_package.html',{'package':package})






















