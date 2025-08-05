from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from randompinfield import RandomPinField
import datetime
from ckeditor.fields import RichTextField
from . import currency

# Create your models here.

class Cargo(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Kargolar"

class Slider(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="slider/")
    link = models.CharField(max_length=200)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Posterler"



class Brand(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Markalar"

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Kategoriler"

class SubModel(models.Model):
    name= models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Modeller"

class Size(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Ölçüler"


class Product(models.Model):
    sku = models.CharField(max_length=100, verbose_name = "Ürün Kodu")
    name = models.CharField(max_length=100, verbose_name = "Ürün Adi")
    brand = models.ForeignKey(SubModel, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "Ürün Modeli")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True, verbose_name = "Ürün Kategorisi")
    size = models.ManyToManyField(Size, verbose_name = "Ürün Ebati")
    content = RichTextField(verbose_name = "Ürün Aciklamasi")
    price = models.FloatField(verbose_name = "Ürün Kodu")
    image = models.ImageField(upload_to="product/", verbose_name = "Ürün Resmi")
    status = models.BooleanField(default=True, verbose_name = "Ürün Durumu")
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Ürünler"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    feature = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name_plural = "Sepetteki Ürünler"

class OrderStatus(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Sipariş Durumları"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    def __str__(self):
        return f"{self.product} - {self.quantity}"



class Order(models.Model):
    order_id = RandomPinField(length=8)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_item = models.ManyToManyField(OrderItem)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, default=6)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, default=6)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"SP-{self.order_id}"
    
    class Meta:
        verbose_name_plural = "Siparişler"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=150)
    person = models.CharField(max_length=250)
    tel = models.CharField(max_length=20)
    vno = models.IntegerField(null=True, blank=True)
    vda = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="user/",)
    adress = models.TextField()
    mail = models.EmailField(null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.IntegerField()
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.company 
    
    class Meta: 
        verbose_name_plural = "Cariler"




    # def __str__(self):
    #     return self.order_id    cargos = models.ForeignKey(Cargo, on_delete=models.CASCADE)