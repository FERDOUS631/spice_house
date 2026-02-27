from django.contrib import admin
from .models import Customer
from .models import Discount
from .models import Category
from .models import Product
from .models import GalleryImage
from .models import ContactMessage
from .models import Add_Phone_Email
from .models import SocialMediaLink
from .models import RestaurantInfo
from .models import EventType
from .models import TableBooking
from .models import RestaurantSettings
from .models import Order
from .models import OrderItem
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'profile_pic', 'date_of_birth']
    list_filter = ['user', 'phone', 'address', 'profile_pic', 'date_of_birth']
    search_fields = ['user', 'phone', 'address', 'profile_pic', 'date_of_birth']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'code', 'percentage', 'valid_from', 'valid_to']
    list_filter = ['name', 'title', 'code', 'percentage', 'valid_from', 'valid_to']
    search_fields = ['name', 'title', 'code', 'percentage', 'valid_from', 'valid_to']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'del_price', 'price', 'description', 'category']
    list_filter = ['category','name']
    search_fields = ['name', 'del_price', 'price', 'description', 'category']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_filter = ['title']
    search_fields = ['title']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'created_at']
    list_filter = ['name', 'email', 'subject', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'created_at']

@admin.register(Add_Phone_Email)
class Add_Phone_EmailAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'location', 'location_link']
    list_filter = ['phone', 'email', 'location']
    search_fields = ['phone', 'email', 'location']

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['fb_link', 'twitter_link', 'instagram_link', 'linkedin_link', 'printerest_link', ]
    search_fields = ['fb_link', 'twitter_link', 'instagram_link', 'linkedin_link', 'printerest_link',]

@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display =['map_iframe']

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'persons', 'event_type', 'date', 'time', 'message']
    list_filter = ['name', 'email', 'phone', 'persons', 'event_type', 'date', 'time']
    search_fields = ['name', 'email', 'phone', 'persons', 'event_type__name', 'date', 'time', 'message']


@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    list_display = ['total_tables']
    search_fields = ['total_tables']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name','user', 'total_amount', 'created_at', 'in_paid', 'transaction_id']
    list_filter = ['full_name','user', 'total_amount', 'created_at']
    search_fields = ['full_name','user', 'total_amount', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product', 'quantity', 'price']
    search_fields = ['order', 'product', 'quantity', 'price']

# change dashboard title my reurant
admin.site.site_header = 'Spice House Admin'
admin.site.index_title = 'Welcome to Spice House Admin'
admin.site.site_title = 'Spice House Admin'

       