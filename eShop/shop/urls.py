from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60) (HomePage.as_view()), name='home'),
    path('category/<str:slug>/', GetCategory.as_view(), name='category'),
    path('search/', Search.as_view(), name='search'),
    path('product/<str:slug>', ProductDetail.as_view(), name='product_detail'),
    path('product-list/', ProductList.as_view(), name='product_list'),
    path('product-list/filter_by_price/', filterr, name='price_filtered'),
    path('shipping-policy/', cache_page(60)(shipping_policy), name='shipping_policy'),
    path('return-policy/', cache_page(60)(return_policy), name='return_policy'),
    path('payment-policy/', cache_page(60)(payment_policy), name='payment_policy'),
    path('privacy-policy/', cache_page(60)(privacy_policy), name='privacy_policy'),
    path('terms-conditions/', cache_page(60)(terms_conditions), name='terms_conditions'),
    path('about-us/', cache_page(60)(about_us), name='about_us'),
    path('contact-us/', contact_us, name='contact_us'),
    path('subscribe-email', subscribe_email, name='subscribe_email'),
    path('registration/', registrate, name='register'),
    path('login/', Userlogin, name='login'),
    path('logout/', Userlogout, name='logout'),
    path('user/<int:pk>', Profile.as_view(), name='profile'),
    path('brand/<str:slug>', GetBrand.as_view(), name='brand'),
    path('user/<int:pk>/change-data', change_account_data, name='change_general_data'),
    path('user/<int:pk>/change-password', change_account_password, name='change_password'),
    path('product/<int:pk>/add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('product/<int:pk>/remove-from-wishlist/', remove_from_wishlist, name='remove_from_wishlist'),
    path('user/<int:pk>/wishlist', Wishlist.as_view(), name='wishlist'),
    path('user/<int:pk>/add-to-cart', add_to_cart, name='add_to_cart'),
    path('user/<int:pk>/cart', Cart.as_view(), name='cart'),
    path('user/<int:pk>/remove-from-cart', remove_from_cart, name='remove_from_cart'),
    path('product/<int:pk>/create_comment', submit_comment, name='submit_comment'),
    path('product/<int:pk>/make_order', order, name='make_order'),

]