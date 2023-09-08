from django.db import models 
from django.contrib.auth.models import AbstractUser 

from uuid import uuid4 

from main.constants import QTY_UNIT_CHOICES, GENDER_CHOICES, ORDER_STATUS_CHOICES

class BaseModel(models.Model): 

    id = models.UUIDField(primary_key=True, default=uuid4) 
    created_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='created_%(class)s', related_query_name='created_%(class)s') 
    updated_by = models.ForeignKey('User', on_delete=models.PROTECT, related_name='updated_%(class)s', related_query_name='updated_%(class)s')  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    is_archived = models.BooleanField(default=False) 

    class Meta: 
        abstract = True

class User(BaseModel, AbstractUser): 
    date_joined = models.DateField(auto_now=True)
    gender = models.CharField(max_length=255, null=True, choices=GENDER_CHOICES) 
    birth_date = models.DateField(null=True)

    class Meta: 
        db_table = 'user' 
    
    def __str__(self): 
        return self.username 
    
class Supplier(BaseModel): 
    name = models.CharField(max_length=255) 
    email = models.EmailField(max_length=255, null=True)
    contact_no = models.CharField(max_length=13, null=True) 

    class Meta: 
        db_table = 'supplier' 
    
    def __str__(self): 
        return self.name 
    
class Client(BaseModel): 
    name = models.CharField(max_length=255) 
    email = models.EmailField(max_length=255, null=True) 
    contact_no = models.CharField(max_length=13, null=True) 

    class Meta: 
        db_table = 'client' 
    
    def __str__(self): 
        return self.name 

class Material(BaseModel): 
    name = models.CharField(max_length=255, null=True) 
    price = models.FloatField() 
    tax = models.FloatField() 
    qty_unit = models.CharField(max_length=255, choices=QTY_UNIT_CHOICES) 
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT) 

    class Meta: 
        db_table = 'material' 

    def __str__(self): 
        return self.name 

class Stock(BaseModel): 
    material = models.ForeignKey(Material, on_delete=models.PROTECT) 
    quantity = models.IntegerField() 

    class Meta: 
        db_table = 'stock' 
    
    def __str__(self): 
        return f'{self.mateiral} - {self.quantity}'
    

    

class Product(BaseModel): 
    description = models.TextField() 
    name = models.CharField(max_length=255, null=False) 
    price = models.FloatField() 
    tax = models.FloatField() 
    qty_unit = models.CharField(max_length=255, choices=QTY_UNIT_CHOICES) 
    materials = models.ManyToManyField(Material, through='ProductMaterial') 

    class Meta: 
        db_table = 'product' 

    def __str__(self): 
        return self.name 
    
class ProductMaterial(BaseModel): 
    product = models.ForeignKey(Product, on_delete=models.PROTECT) 
    material = models.ForeignKey(Material, on_delete=models.PROTECT) 
    quantity = models.IntegerField() 
    comment = models.TextField() 

    class Meta: 
        db_table = 'productmaterial' 
        
    def __str__(self): 
        return f'{self.material} - {self.product}' 

class Purchase(BaseModel): 
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT) 
    material = models.ForeignKey(Material, on_delete=models.PROTECT) 
    quantity = models.IntegerField(default=0) 
    qty_unit = models.CharField(max_length=255, choices=QTY_UNIT_CHOICES, null=True) 
    requested_at = models.DateTimeField(null=True) 
    requested_user = models.ForeignKey(User, on_delete=models.PROTECT)
    arrived_at = models.DateTimeField(null=True) 
    is_arrived = models.DateTimeField(null=True) 

    class Meta: 
        db_table = 'purchase' 

    def __str__(self): 
        return f'{self.material} - {self.supplier}'

class Order(BaseModel): 
    client = models.ForeignKey(Client, on_delete=models.PROTECT) 
    order_status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES[0][0])
    requested_at = models.DateTimeField(null=True)
    request_user = models.DateTimeField(null=True) 
    finished_at = models.DateTimeField(null=True) 
    comment = models.CharField(max_length=255, null=True) 

    class Meta: 
        db_table = 'order' 

    def __str__(self): 
        t = self.requested_at.strftime('%d:%m:%y')
        return f'{self.client} - {str(t)}'
    
class OrderProduct(BaseModel): 
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField() 

    class Meta: 
        db_table = 'orderproduct' 
    
    def __str__(self): 
        return f'{self.product} - {str(self.quantity)}'
    
class MaterialConsumption(BaseModel): 
    order_product = models.ForeignKey(OrderProduct, on_delete=models.PROTECT) 
    material = models.ForeignKey(Material, on_delete=models.PROTECT) 
    quantity = models.IntegerField() 
    is_allocated = models.BooleanField(default=False) 
    comment = models.TextField() 

    class Meta: 
        db_table = 'materialconsumption' 

    def __str__(self): 
        return f'{self.material} - {self.order_product}'
    

