from  .models import Category
from  .models import Product
from .models import GalleryImage
from .models import Add_Phone_Email
from .models import SocialMediaLink
from .models import RestaurantInfo
from .cart import Cart

def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}   

def products(request):
    products = Product.objects.all().order_by('-id')
    return {'products': products}
def gallery_images(request):
    gallery_images = GalleryImage.objects.all().order_by('-id')
    return {'gallery_images': gallery_images}

def contact_info(request):
    contact_info = Add_Phone_Email.objects.all().order_by('-id')
    return {'contact_info': contact_info}
def social_links(request):
    social_links = SocialMediaLink.objects.all().order_by('-id')
    return {'social_links': social_links}
def restaurant_info(request):
    restaurant_info = RestaurantInfo.objects.all().order_by('-id')
    return {'restaurant_info': restaurant_info}
def cart(request):
    return {'cart': Cart(request)}



