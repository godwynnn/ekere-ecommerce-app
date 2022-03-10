
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home_page, name='home'),
    path('ekere-new/',Create_page, name='create'),
    # path('ekere/<slug:slug>/<int:id>/',Detail_page,name='detail'),
    path('ekere/<slug:slug>/<str:id>/edit',update_page,name='update'),
    path('ekere/<slug:slug>/<str:id>/delete',Delete_page,name='delete'),
    path('ekere-signup/',Signup_page,name='signup'),
    path('ekere-signin/',Signin_view,name='login'),
    path('search/',Search_page,name='search'),
    path('checkout/',Checkout_page,name='checkout'),
    path('cart/',Cart_view,name='cart'),
    path('success/',Success_page,name='cancel'),
    path('cancel/',Cancel_page,name='success'),
    path('dashboard/',Dashboard,name='dashboard'),
    path('create_payment/',Create_payment,name='create_payment'),
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
