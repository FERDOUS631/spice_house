from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=15) 
    address = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/%Y/%m/%d', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
      
        return self.user.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

class Discount(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='discounts/%Y/%m/%d', null=True, blank=True)
    title = models.CharField(max_length=500)
    code = models.CharField(max_length=20, null=True, blank=True,)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/%Y/%m/%d', unique=True)
    del_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        
        return self.name
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', unique=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name} - {self.subject}'
    
    class Meta:
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

class Add_Phone_Email(models.Model):
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=100)
    location_link = models.URLField(max_length=500,unique=True)


    def __str__(self):
        return self.location

    class Meta:
        verbose_name = 'Add Phone Email'
        verbose_name_plural = 'Add Phone Emails'

class SocialMediaLink(models.Model):
    fb_link = models.URLField(max_length=200, null=True, blank=True ,default='https://www.facebook.com/')
    twitter_link = models.URLField(max_length=200, null=True, blank=True, default='https://www.twitter.com/')
    instagram_link = models.URLField(max_length=200, null=True, blank=True, default='https://www.instagram.com/')
    linkedin_link = models.URLField(max_length=200, null=True, blank=True, default='https://www.linkedin.com/')
    printerest_link = models.URLField(max_length=200, null=True, blank=True, default='https://www.pinterest.com/')
    def __str__(self):
        return "Social Media Links"
    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'

class RestaurantInfo(models.Model):

    map_iframe = models.TextField(help_text="Add embedded Google Maps iframe code here", blank=True, null=True)

    def __str__(self):
        return f"location google map{self.id}"
    class Meta:
        verbose_name = 'Location Google Map'
        verbose_name_plural = 'Location Google Maps'

class EventType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Add Event Programme Type'
        verbose_name_plural = 'Add Event Programme Types'

class TableBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    persons = models.PositiveIntegerField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

class RestaurantSettings(models.Model):
    total_tables = models.PositiveIntegerField(
        default=20, 
        help_text="Enter the total number of tables available in your restaurant."
    )
    min_booking_hours = models.PositiveIntegerField(
        default=2, 
        help_text="How many hours in advance should a customer book?"
    )
    special_notice = models.TextField(
        blank=True, 
        null=True, 
        help_text="Any urgent message (e.g., 'Closed for a private party today')."
    )

    class Meta:
        verbose_name = "Restaurant Setting"
        verbose_name_plural = "Restaurant Settings"

    def __str__(self):
        return "Global Restaurant Settings"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    in_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"Order {self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} - {self.product.name}"






        
    
    


