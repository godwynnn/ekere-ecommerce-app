"""ekere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from ekereapp.models import EkerePost
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from ekereapp.views import(
     home_page,
     create_page,
    #  detail_page,
     update_page,
     delete_page,
     signup_page,
     signin_view,
    #  search_view,
     Logout_view,
     Add_to_cart,Cart_view,Remove_from_cart,Remove_single_item,
     Address_page,Success_page,create_payment,Checkout_page,
     Cancel_page,Dashboard,Search_page,Check_Carted


)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(''ekereapp.urls),
    

]


# if settings.DEBUG:



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
