from django.contrib import admin
from .models import *
import csv
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['name', 'content']
    list_display = ['sku', 'name', 'price', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Brand)
admin.site.register(Cargo)
#admin.site.register(Order)
#admin.site.register(OrderItem)
admin.site.register(OrderStatus)
admin.site.register(Profile)
admin.site.register(SubModel)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Slider)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id','status', 'user', 'cargo','created')

admin.site.register(Order, OrderAdmin)


# def import_products_from_excel(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             sku = row['sku']
#             name = row['name']
            
#             content = row['content']
#             price = float(row['price'])
#             status = True 
#             product = Product.objects.create(
#                 sku=sku,
#                 name=name,
#                 content=content,
#                 price=price,
#                 status=status
#             )
#             print(f"Ürün oluşturuldu: {product}")