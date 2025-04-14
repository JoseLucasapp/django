from django.contrib import admin
from .models import Category, Product, Client, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available',
                    'created_at', 'category')
    list_filter = ('available', 'created_at', 'category')
    search_fields = ('name',)
    autocomplete_fields = ('category',)
    date_hierarchy = 'created_at'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'born_date', 'is_active')
    list_filter = ('is_active', 'born_date')
    search_fields = ('full_name', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "get_products", "amount", "created_at")
    list_filter = ("created_at", "client", "products")
    search_fields = ("client__full_name", "products__name")

    def get_products(self, obj):
        return ", ".join([product.name for product in obj.products.all()])
    get_products.short_description = "Products"
