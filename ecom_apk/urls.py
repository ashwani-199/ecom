from django.urls import path
from ecom_apk import views
urlpatterns = [
    path('',views.index,name="index"),   
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'), 
    path('contact',views.contact,name="contact"),   
    path('about',views.about,name="about"), 
    path('profile',views.profile,name="profile"), 
    path('checkout/',views.checkout,name="Checkout"),
    
]
