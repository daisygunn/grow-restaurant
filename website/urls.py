from . import views
from django.urls import path, include
from django.conf.urls import include, url

urlpatterns = [
    path('', views.index, name='index'),
    path('contact_us', views.ContactPage.as_view() , name='contact_us'),
    
]