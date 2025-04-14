from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Client(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    born_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


class Order(models.Model):
    client = models.ForeignKey("Client", on_delete=models.CASCADE)
    products = models.ManyToManyField("Product", through="OrderItem")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount(self):
        total = sum(item.get_total_price()
                    for item in self.orderitem_set.all())
        return total

    def __str__(self):

        return f"Client: {self.client},\nAmount: {self.amount},\nCreated at: {self.created_at},\nProducts: {', '.join([product.name for product in self.products.all()])}\n"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
