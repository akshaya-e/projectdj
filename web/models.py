from django.db import models
from django.contrib.auth.models import AbstractUser,timezone,User

# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
        #('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username   

    
class Package(models.Model):
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    image = models.ImageField(upload_to='package_images/', blank=True, null=True)
    approved = models.BooleanField(default=False)
    vendor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'vendor'},
        related_name='packages'
    )
    expiry_date=models.DateTimeField(default=timezone.now)
    #expiry_date = models.DateField()

@property
def is_expired(self):
    return timezone.now()
def __str__(self):
        return f"{self.title} - {self.destination}"
    
    
    
class Booking(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='bookings')
    package = models.ForeignKey(Package,on_delete=models.CASCADE,related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20,choices=[('pending', 'Pending'),('completed', 'Completed'),('failed', 'Failed')],default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by{self.user.username} for {self.package.title}"
    
    
    
class Vendor(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=50)
    address=models.TextField()
    
    def __str__(self):
        return self.company_name
    
