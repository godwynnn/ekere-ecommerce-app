from http.client import HTTPResponse
from math import prod
from multiprocessing import context
from turtle import title
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from .decorators import authenticated_user,allowed_user
from django.db.models import Q
from django.contrib.auth.models import Group
# from django.contrib.sessions.backends.db import SessionStore 
# from django.contrib.sessions.models import Session
import uuid
from django.core.paginator import Paginator
from django.conf import settings
# Create your views here.

import base64
import json
import os
import stripe
from django.http import JsonResponse,HttpResponse,Http404
# session=SessionStore()
def  Home_page(request):
    
    # print(request)
    if "member_id" in request.session:

        member_id=str(uuid.uuid4())
        member_id=request.session["member_id"]
        print('USER ID' + member_id)
    
    else:
        member_id=str(uuid.uuid4())
        request.session["member_id"]=member_id
    
    
    member_id=request.session["member_id"]
    request.session.modified= True
    request.session.set_expiry(0)

    cart_qs=Cart.objects.filter(member_id=member_id,ordered=False).first()
    total_goods=''

    
    query_obj=Product.objects.all()
    p=Paginator(query_obj,8)
    page_no=request.GET.get('page')
    query=p.get_page(page_no)

    # carted_in=False
    # if cart_qs:
    #     total_goods=cart_qs.total_count()
    #     cart=cart_qs
        # for object in query:
        # if order_item in cart.items.all():
        #     carted_in=True

    template='ekere/home.html'
    context={"objects": query,
         
            'total_goods':total_goods,
            
        }
    return render(request,template,context)


def Check_Carted(request,slug):
    member_id=request.session["member_id"]
    product=Product.objects.get(slug=slug)
    cart_qs=Cart.objects.filter(member_id=member_id,ordered=False).first()
    order_item=Orderitem.objects.get(ordered=False,item=product)
    carted=False
    if order_item in cart_qs.items.all():
        carted=True
    template='ekere/home.html'
    context={'cart':cart_qs,'order_item':order_item,'carted':carted}
    return render(request,template,context)

@allowed_user
def create_page(request):
    form=EkerePostForm(request.POST or None)
    if form.is_valid:
        if request.method=='POST':
            qs=form.save(commit=False)
            qs.slug=slugify(qs.title+ "-"+qs.content[:10])
            qs.save()
            form=EkerePostForm()
    template='ekere/create.html'
    context={"form":form}
    return render(request,template,context)

@allowed_user
def Update_page(request, id,slug):
    query=Product.objects.get(id= id, slug=slug)
    form=EkerePostForm(request.POST or None, instance=query)
    if request.method=='POST':
        if form.is_valid:
        
            form.save()
            form=EkerePostForm()
    template='ekere/edit.html'
    context={"form":form}
    return render(request,template,context)

@allowed_user
def Delete_page(request,slug,id):
    query=Product.objects.get(id=id,slug=slug)
    query.delete()
    return redirect("/index")
    return render(request)

@authenticated_user
def Signup_page(request):
    group=None
    form=UserForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
        
            user=form.save()
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            user.save()
            username=form.cleaned_data['username']
            messages.success(request,'you have successfully created an account for '+ username)
            form=UserForm()
            return redirect('/ekere-signin')
    template='ekere/signup.html'
    context={"form":form}
    return render(request,template,context)


@authenticated_user
def Signin_view(request):
    # member_id=request.session['member_id']
    # print('USER ID' + member_id)
    if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']

            user=authenticate(request,email=username,password=password)
            if user is not None:
                login(request,user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home')
            else:
                messages.info(request,"incorrect Email OR Password")

    template='ekere/login.html'
    return render(request,template)

    

def Logout_view(request):
   
    # del request.session['member_id']
    # member_id=request.session['member_id']
    # print('USER ID' + member_id)
    logout(request)
    return redirect('home')
    


def Cart_view(request):
    member_id=request.session['member_id']
    cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
    product_price=''
    total_price=''
    total_goods=''
    if cart:
        total_goods=cart.total_count()
        product_price=cart.summed_product_price()
        total_price=cart.total_price()
    context={'cart':cart,'product_price':product_price,'total_price':total_price,'total_goods':total_goods}
    return render(request,'ekere/cart.html',context)


def Add_to_cart(request,slug):
    product=Product.objects.get(slug=slug)
    member_id=request.session['member_id']
    
    
    # user=request.user
    if request.user.is_authenticated:
        
        member_id=request.session['member_id']
        order_p=Orderitem.objects.filter(member_id=member_id)
        if order_p.exists():
            # order_item=order_p.first()
            order_item, created=Orderitem.objects.get_or_create(item=product,member_id=member_id,ordered=False)
            print('USER ID' + member_id)
        else:     
            
            order_item, created=Orderitem.objects.get_or_create(item=product,member_id=member_id,ordered=False,user=request.user)
            # order_qs=Cart.objects.filter(member_id=member_id,ordered=False)
    
    else:
        member_id=request.session['member_id']
        print('USER ID'+ member_id)

        order_item, created=Orderitem.objects.get_or_create(item=product,member_id=member_id,ordered=False)

    order_item, created=Orderitem.objects.get_or_create(item=product,member_id=member_id,ordered=False)
    order_qs=Cart.objects.filter(member_id=member_id,ordered=False)
    if order_qs.exists():
        order=order_qs.first()
       
        if order.items.filter(item__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            # messages.info(request, "This item quantity was updated.")
            return HttpResponseRedirect(reverse('cart'))
        else:
            order.items.add(order_item)
            # messages.info(request,'product added to cart')
            return HttpResponseRedirect(reverse('cart'))
    
    else:
        try:
            user=request.user
            member_id=request.session['member_id']
            if request.user.is_authenticated:
                
                if Cart.objects.filter(member_id=member_id).first().exists():
                    order=Cart.objects.get_or_create(member_id=member_id)
                    order.items.add(order_item)
                    # messages.info(request,'just added to cart')
                    return HttpResponseRedirect(reverse('cart'))
            else:
                order=Cart.objects.create(member_id=member_id)
                order.items.add(order_item)
                # messages.info(request,'just added to cart')
                return HttpResponseRedirect(reverse('cart'))
        except:
            member_id=request.session['member_id']
            order=Cart.objects.create(member_id=member_id)
            order.items.add(order_item)
            # messages.info(request,'just added to cart')
            return HttpResponseRedirect(reverse('cart'))


def Remove_from_cart(request,slug):
    product=Product.objects.get(slug=slug)
    member_id=request.session['member_id']

    order_item=Orderitem.objects.filter(member_id=member_id,ordered=False,item=product).first()
    cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
    if cart:
        if order_item in cart.items.all():
            cart.items.remove(order_item)
            order_item.delete()
            # cart.delete()
            
            # messages.info(request, "This item was removed from your cart.")
            return HttpResponseRedirect(reverse('cart'))
        else:
            cart.delete()
            # messages.info(request, "This item was not in your cart")
            # return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        # return redirect("core:product", slug=slug)

def Remove_single_item(request,slug):

    product=Product.objects.get(slug=slug)
    member_id=request.session['member_id']

    order_item=Orderitem.objects.filter(member_id=member_id,ordered=False,item=product).first()
    cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
    if cart:
       
        if order_item in cart.items.all():
            if order_item.quantity > 1:
                order_item.quantity-=1
                order_item.save()
                return HttpResponseRedirect(reverse('cart'))
            else:
                cart.items.remove(order_item)
                order_item.delete()
                # cart.delete()
                # messages.info(request, "This item quantity was updated.")
                return HttpResponseRedirect(reverse('cart'))
        else:
            # messages.info(request, "This item was not in your cart")
            return HttpResponseRedirect(reverse('cart'))
    else:
        # messages.info(request, "You do not have an active order")
        return HttpResponseRedirect(reverse('cart'))


@login_required(login_url='login')
def Address_page(request):
    member_id=request.session['member_id']
    cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
    form=AddressForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid:
            addr=form.save(commit=False)
            addr.member_id=member_id
            addr.user=request.user
            addr.default=True
            addr.save()
            form=AddressForm()
            address=Address.objects.filter(member_id=member_id,default=True,user=request.user).first()
            cart.addr=address
            cart.save()
            return redirect('create_payment')
           
        
    context={'form': form,
            'total_amount':cart.total_price(),
            'cart':cart
        }
    return render(request,'ekere/address.html',context)



# @login_required(login_url='login')
# def calculate_order_amount(request,items):
#     # Replace this constant with a calculation of the order's amount
#     # Calculate the order total on the server to prevent
#     # people from directly manipulating the amount on the client
#     member_id=request.session['member_id']
#     cart=Cart.objects.filter(member_id=member_id,ordered=False).first()

#     return cart.total_price()






@login_required(login_url='login')
def Create_payment(request):
    member_id=request.session['member_id']
    cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
    items=''
    for product in cart.items.all():
        items=product
    DOMAIN='ekere-ecomm.herokuapp.com/'    
    stripe.api_key = settings.STRIPE_SECRET
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name':  items,
            },
            'unit_amount': cart.total_price()*100,
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url=DOMAIN+'success',
        cancel_url=DOMAIN+'cancel',
    )

    return redirect(session.url, code=303)


@login_required(login_url='login')
def Checkout_page(request):
    member_id=request.session['member_id']
    try:
        cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
    except:
        raise Http404
    total_amount=cart.total_price()
    context={'total_amount':total_amount}
    return render(request,'ekere/checkout.html',context)

@login_required(login_url='login')
def Success_page(request):
    member_id=request.session['member_id']
    
    cart=Cart.objects.filter(member_id=member_id,ordered=False).first()
   
    
    for item in cart.items.all():
        
        item.ordered=True
        item.user=request.user
        item.save()
    cart.addr.default=True
    cart.user=request.user
    cart.ordered=True
    cart.save()
    
    return render(request,'ekere/success.html')


@login_required(login_url='login')
def Cancel_page(request):

   
    return render(request,'ekere/cancel.html')


@login_required(login_url='login')
def Dashboard(request):
    form=UserProfileform(request.POST or None,request.FILES or None)
    # user=UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            
            return redirect('dashboard')
    else:
        form=UserProfileform()
    cart=Cart.objects.filter(ordered=True,user=request.user)
    obj=Userprofile.objects.filter(user=request.user).first()
    context={'cart': cart,'form':form,
            'total_orders':cart.count(),
            'object':obj
    }
    return render(request,'ekere/dashboard.html',context)


def Search_page(request):
    query=request.GET.get('q')
    tag=''
    
    query_product=Product.objects.filter(
        Q(title__icontains=query)|
        Q(price__icontains=query)|
        Q(tags__name__icontains=query)
    )
    template='ekere/home.html'
    context={"query": query,'query_product': query_product}
    return render(request,template,context)
