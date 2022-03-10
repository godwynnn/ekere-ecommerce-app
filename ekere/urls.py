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
    path('index/',home_page, name='home'),
    path('ekere-new/',create_page, name='create'),
    # path('ekere/<slug:slug>/<int:id>/',detail_page,name='detail'),
    path('ekere/<slug:slug>/<str:id>/edit',update_page,name='update'),
    path('ekere/<slug:slug>/<str:id>/delete',delete_page,name='delete'),
    path('ekere-signup/',signup_page,name='signup'),
    path('ekere-signin/',signin_view,name='login'),
    path('search/',Search_page,name='search'),
    path('checkout/',Checkout_page,name='checkout'),
    path('cart/',Cart_view,name='cart'),
    path('success/',Success_page,name='cancel'),
    path('cancel/',Cancel_page,name='success'),
    path('dashboard/',Dashboard,name='dashboard'),
    path('create_payment/',create_payment,name='create_payment'),
    path('check-carted/',Check_Carted,name='check_carted'),
    path('address/',Address_page,name='address'),
    path('logout/',Logout_view,name='logout'),
    path('add_to_cart/<str:slug>/',Add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<str:slug>/',Remove_from_cart,name='remove_from_cart'),
    path('remove_single_item/<str:slug>/',Remove_single_item,name='remove_single_item'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='change-password.html'), name='password_change'),
    path('password-changed/',auth_views.PasswordChangeDoneView.as_view(template_name='password-changed.html'), name='password_change_done'),


    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')

]


# if settings.DEBUG:


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
