from . import views
from django.urls import path, include
from django.conf.urls import include, url

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact_us', views.ContactPage.as_view() , name='contact_us'),
    # path('menus/', views.menus, name='menus/')
]