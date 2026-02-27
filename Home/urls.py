from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('menu/', views.menu, name='menu'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('book_table/', views.book_table, name='book_table'),
    path('story/', views.story, name='story'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('cart-add/', views.cart_add, name='cart_add'),
    path('cart-update/', views.cart_update, name='cart_update'),
    path('cart-delete/', views.cart_delete, name='cart_delete'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    ]
