from django.utils import timezone
from django.contrib import messages
from urllib import request
from .cart import Cart
from .models import Product
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Customer
from .models import Discount
from .models import ContactMessage
from .models import EventType
from .models import TableBooking
from .models import RestaurantSettings
from .models import Order
from .models import OrderItem
import random
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.



def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

     
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Password does not match'})
        # validation
        if User.objects.filter(username=email).exists():
            return render(request, 'registration.html', {'error': 'Email already exists'})
        if password and len(password) < 6:
            return render(request, 'registration.html', {'error': 'Password must be at least 6 characters'})
        

       
        otp = str(random.randint(100000, 999999))

       
        request.session['register_data'] = {
            'name': name,
            'email': email,
            'number': number,
            'password': password,
            'otp': otp
        }

     
        subject = "Account Verification Code"
        message = f"Hello {name}, your verification code is: {otp}"
        from_email = settings.EMAIL_HOST_USER
        
        try:
            send_mail(subject, message, from_email, [email])
            messages.success(request, f"Your OTP is: {otp_code}")
            return redirect('verify_otp') 
        except Exception as e:
            return render(request, 'registration.html', {'error': 'Email sending failed. Check settings.'})

    return render(request, 'registration.html')


def verify_otp(request):
    register_data = request.session.get('register_data')
    
    if not register_data:
        return redirect('register')

    if request.method == 'POST':
        user_otp = request.POST.get('otp')

        if user_otp == register_data['otp']:
            
            user = User.objects.create_user(
                username=register_data['email'],
                email=register_data['email'],
                password=register_data['password'],
                first_name=register_data['name']
            )
            Customer.objects.create(user=user, phone=register_data['number'])
            
           
            del request.session['register_data']
            
            return render(request, 'registration.html', {'success': 'Account verified and created!'})
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP!'})

    return render(request, 'verify_otp.html')

def user_login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            context = {
                'login_status': 'User logged in successfully'
            }
            return redirect('index')
        else:
            context = {
                'login_status': 'Invalid email or password'
            }
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)

def index(request):

    if request.user.is_authenticated:
        discounts = Discount.objects.all().order_by( '-id')
        settings = RestaurantSettings.objects.first()
        total_tables = settings.total_tables if settings else 20
        today = timezone.now().date()
        booked_tables = TableBooking.objects.filter(date=today).count()
        available_tables = total_tables - booked_tables

   
        
        context = {
            'discounts': discounts,
            'total_tables': total_tables,
            'booked_tables': booked_tables,
            'available_tables': available_tables,
            'settings': settings,
        }
        return render(request, 'index.html', context)
    
    else:

        return redirect('about')


def user_logout(request):
    logout(request)
    return redirect('login')

# menu view
@login_required(login_url='login')
def menu(request):
    return render(request, 'menu.html')

def profile(request):
    profile = Customer.objects.filter(user=request.user).first()
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.first_name = request.POST.get('name')
        user.last_name = request.POST.get('last_name')
        user.save()

        profile.phone = request.POST.get('contact')
        profile.address = request.POST.get('address')

        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']
        elif request.POST.get('remove_profile_pic') == 'true':
            profile.profile_pic = 'profile_pics/default_picture.png'
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile})


def about(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('about')
    return render(request, 'about.html')
@login_required(login_url='login')
def book_table(request):
    event_types = EventType.objects.all() 
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        persons = request.POST.get('persons')
        event_id = request.POST.get('event_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message_text = request.POST.get('message')

       
        event_obj = EventType.objects.get(id=event_id)
        TableBooking.objects.create(
            name=name, email=email, phone=phone,
            persons=persons, event_type=event_obj,
            date=date, time=time, message=message_text
        )
        
        messages.success(request, f'Dear {name} sir,Your table booking request has been sent successfully for {event_obj.name} event ! We will contact you soon.')
        return redirect('book_table')

    return render(request, 'book_table.html', {'event_types': event_types})

def story(request):
    return render(request, 'story.html')





def cart_summary(request):
    cart = Cart(request)
    if cart.__len__() == 0:
        messages.info(request, "Your cart is empty! Add some food to proceed.")
        return redirect('menu')
    cart_products = []
    for p_id, item in cart.cart.items():
        product = get_object_or_404(Product, id=p_id)
        cart_products.append({
            'product': product,
            'quantity': item['qty'],
            'total_price': Decimal(item['price']) * item['qty']
        })
    return render(request, 'cart_summary.html', {'cart_items': cart_products, 'total': cart.get_total()})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        return JsonResponse({'qty': cart.__len__()})


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        todo = request.POST.get('todo')
        cart.update(product_id=product_id, action=todo)
        
       
        qty = cart.cart[str(product_id)]['qty']
        return JsonResponse({
            'qty': qty,
            'total': cart.get_total(),
            'cart_count': cart.__len__()
        })

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product_id=product_id)
        return JsonResponse({
            'total': cart.get_total(),
            'cart_count': cart.__len__()
        })
    
@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    return render(request, 'checkout.html', {'cart': cart, 'total': cart.get_total()})
    

def place_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        if cart.__len__() == 0:
           messages.info(request, 'Your cart is empty')
           return redirect('checkout')
        

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            total_amount=cart.get_total(),
            payment_method=payment_method,
            transaction_id=str(uuid.uuid4())[:10].upper()
        )

        for p_id, item in cart.cart.items():
            product = get_object_or_404(Product, id=p_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['qty'],
                price=item['price']
            )

        if payment_method == 'cod':
            cart.clear()
           
            return redirect('order_success', order_id=order.id)
        else:
            messages.info(request, "Online payment is currently unavailable. Please use Cash on Delivery.")
            order.delete()
            return redirect('checkout')

    return redirect('checkout')
def order_success(request, order_id):
    try:
      
        order_id= Order.objects.get(id=order_id)
        return render(request, 'order_success.html', {
            'order': order_id, 
            'method': 'Cash on Delivery (COD)'
        })
    except Order.DoesNotExist:
        return redirect('home')