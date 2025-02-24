from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.home, name='home'),
    path('register/', v.register, name='register'),
    path('login/', v.user_login, name='login'),
    path('logout/', v.user_logout, name='logout'),
    path('packages/', v.list_packages, name='list_packages'),
    path('packages/create/', v.create_package, name='create_package'),
    path('packages/<int:package_id>/book/', v.book_package, name='book_package'),
    path('packages/pending/', v.pending_packages, name='pending_packages'),
    path('admin/packages/approve/<int:package_id>/', v.approve_package, name='approve_package'),
    path('packages/edit/<int:package_id>',v.edit_package,name='edit_package'),
    path('packages/delete/<int:package_id>',v.delete_package,name='delete_package'),
    
   
]
