# from email.policy import default
# from enum import unique
# from pyexpat import model
# from typing_extensions import Required
# from typing_extensions import Required
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify



# Create your models here.
class User(AbstractUser):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=200)
    birth_day=models.DateField(null=True)
    # image=models.ImageField(upload_to='profile_pic/', null=True,blank=True,)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['username']
 

    def __str__(self):
        return self.email


class Userprofile(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pic/', null=True,blank=True, default='user.png')

    class Meta:
        ordering=['-id']

    def __str__(self):
        return f"{self.user} - picture"



class Tag(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length= 200)
    image=models.ImageField(upload_to='image', blank=True,null=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    content=models.TextField(blank=True,null=True)
    tags=models.ManyToManyField(Tag)
    price=models.PositiveIntegerField(blank=True,null=True,default=0)
    date_added=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now= True)

    class Meta:
        ordering=['-date_added']

    def save(self, *args,**kwargs):
        if self.slug == None:
            slug=slugify(self.title)
            has_slug=Product.objects.filter(slug=slug)
            count =1
            while has_slug:
                count +=1
                slug=slugify(self.title) + '-' + str(count)
                has_slug=Product.objects.filter(slug=slug).exists()

            self.slug=slug
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


class Orderitem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    item=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    member_id=models.CharField(max_length=1000, null=True,blank=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"orders-{self.item.title}- {self.quantity}"

    def product_price(self):
        return self.quantity*self.item.price



ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,null=True,blank=True)
    street_address = models.TextField(max_length=100)
    country = models.CharField(max_length=50)
    member_id=models.CharField(max_length=1000, null=True,blank=True)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1000, choices=ADDRESS_CHOICES,default='B')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Cart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    addr=models.ForeignKey(Address,blank=True,null=True,on_delete=models.CASCADE)
    items=models.ManyToManyField(Orderitem)
    member_id=models.CharField(max_length=1000, null=True,blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
    
        return self.member_id

    def summed_product_price(self):
        for product in self.items.all():
            return product.product_price()
        
    def total_price(self):
        total=0
        for product in self.items.all():
            total += product.product_price()
        return total

    def total_count(self):
        return self.items.count()
class QuerySearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query=models.CharField(max_length=500)
    date_searched=models.DateTimeField(auto_now_add=True)


