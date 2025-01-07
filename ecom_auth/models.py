from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()

 
    def __str__(self):
        return self.name
    

class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=70)
    category=models.CharField(max_length=70)
    subcategory=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    image=models.ImageField(upload_to='images/images')

    def __str__(self) :
        return self.product_name
    
class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    address=models.CharField(max_length=150)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    size=models.CharField(max_length=50,default="")
    zip_code=models.CharField(max_length=100)
    phone=models.CharField(max_length=100,default="")
    oid=models.CharField(max_length=150,blank=True)
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    payment_status=models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.name
    
class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    deliverd=models.BooleanField(default=False)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."