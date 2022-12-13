from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import *
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.


class HomePage(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'E Store'
        context['product_featured'] = Product.objects.filter(featured=True)
        context['categories'] = Category.objects.all()
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        return context

class GetCategory(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['productt'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        return context

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

class Search(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'product'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Search - {self.request.GET.get('s')}"
        context['categories'] = Category.objects.all()
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        return context

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("s"))

class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Product.objects.get(slug=self.kwargs['slug'])
        context['pproducts'] = Product.objects.filter(pk__lte=10)
        context['products_all'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        context['brands'] = Brands.objects.all()
        context['comments'] = Comments.objects.filter(product_of_comment=self.get_object())
        return context

class ProductList(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'product'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products'
        context['productt'] = Product.objects.all()
        context['brands'] = Brands.objects.all()
        context['categories'] = Category.objects.all()
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        return context

class ProductListByPrice(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products'
        context['categories'] = Category.objects.all()
        context['brands'] = Brands.objects.all()
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        return context

    def get_queryset(self):
        return Product.objects.filter(Q(price__gte=self.request.GET.get('min_price')) & Q(price__lt=self.request.GET.get('max_price')))

def filterr(request):
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 10000)
    categories = Category.objects.all()
    product = Product.objects.filter(Q(price__gte=min_price) & Q(price__lte=max_price) & Q(name__icontains=request.GET.get('se')))
    sorting = request.GET.get('sorting', '-created_at')
    #product = Product.objects.filter(name__icontains=request.GET.get('se')).filter(price__lte=min_price).filter(price__gte=max_price)
    pag = Paginator(product, 6)
    page_number = request.GET.get('page')
    page_obj = pag.get_page(page_number)



    context = {
        'product': product.order_by(sorting),
        'productt': Product.objects.all(),
        'brands': Brands.objects.all(),
        'title': 'Products',
        'categories': categories,
        's': f"s={request.GET.get('s')}&",
        'sorting': sorting,
        'min_price': min_price,
        'max_price': max_price,
        'page-obj': page_obj,
    }
    return render(request, 'shop/product-list.html', context=context)

def shipping_policy(request):
    context = {
        'title': 'Shipping Policy'
    }
    return render(request, 'shop/shippingPolicy.html', context=context)

def return_policy(request):
    context = {
        'title': 'Return Policy'
    }
    return render(request, 'shop/returnPolicy.html', context=context)

def payment_policy(request):
    context = {
        'title': 'Payment Policy'
    }
    return render(request, 'shop/paymentPolicy.html', context=context)

def privacy_policy(request):
    context = {
        'title': 'Privacy Policy'
    }
    return render(request, 'shop/privacyPolicy.html', context=context)

def terms_conditions(request):
    context = {
        'title': 'Terms & Conditions'
    }
    return render(request, 'shop/termsConditions.html', context=context)

def about_us(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'shop/about_us.html', context=context)

def contact_us(request):
    if request.method == 'POST':
        form = EmailContact(request.POST)
        if form.is_valid():
            mail = send_mail(f"Dear, {form.cleaned_data['user_name']}", 'Thank you for... some text', 'couldzet@gmail.com', [form.cleaned_data['user_email']])
            if mail:
                return redirect('home')
            else:
                print('error')
        else:
            print('validation error')
    else:
        form = EmailContact()
    return render(request, 'shop/contact.html', {'form': form, 'title': 'Contact Us'})

def subscribe_email(request):
    form = emailSubscribe(request.POST)
    emaill = request.POST.get('emailSubscribe')
    print(emaill)
    if form.is_valid():
        form.save()
    return redirect(reverse('home'))

def registrate(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password1']
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            messages.success(request, "Congratulations, you have been registered successfully!")
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'shop/registration.html', {'form': form, 'title': 'Registration'})

def Userlogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            account = authenticate(email=email, password=password)
            if account:
                login(request, account)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'shop/custom-login.html', {'form': form, 'title': 'Login'})

def Userlogout(request):
    logout(request)
    return redirect('home')

class Profile(DetailView):
    model = Account
    template_name = 'shop/my-account.html'
    context_object_name = 'account'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['title'] = user.username
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        context['orders'] = Order.objects.filter(user_made_order=user.id)
        return context

class GetBrand(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Brands.objects.get(slug=self.kwargs['slug'])
        context['productt'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        context['brands'] = Brands.objects.all()
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['cart_products'] = Product.objects.filter(users_cart=self.request.user.id)
        return context

    def get_queryset(self):
        return Product.objects.filter(brand__slug=self.kwargs['slug'])

def change_account_data(request, pk):
    form = ChangeAccountDateForm(request.POST)
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')

    #acc = Account.objects.filter(pk=pk).update(email=email, mobile=mobile, address=address)   --- the same as lines below

    acc = Account.objects.get(pk=pk)
    acc.first_name = first_name
    acc.last_name = last_name
    acc.address = address
    acc.email = email
    acc.mobile = mobile
    acc.save()

    print(form.errors.as_data())

    return redirect(reverse('profile', kwargs={"pk": pk}))

def change_account_password(request, pk):
    password = request.POST.get('password')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    acc = Account.objects.get(pk=pk)
    database_password = acc.password
    print(password)
    print(database_password)
    if check_password(password, database_password) and password1 == password2:
        print('passwords matched')
        encrypted_password = make_password(password1)
        acc.password = encrypted_password
        print(encrypted_password)
        acc.save()
        update_session_auth_hash(request, acc)
        return redirect(reverse('login'))
    else:
        print('some error happened')
        messages.error(request, "Passwords didn't match")
        return redirect(reverse('profile', kwargs={'pk': pk}))

def add_to_wishlist(request, pk):
    user = request.user.id
    product = Product.objects.get(pk=pk)
    print(product)

    if product.users_wishlist.filter(id=user).exists():
        product.users_wishlist.remove(user)
    else:
        product.users_wishlist.add(user)

    page = request.META.get('HTTP_REFERER')
    return redirect(page)

def remove_from_wishlist(request, pk):
    user = request.user.id
    product = Product.objects.get(pk=pk)
    product.users_wishlist.remove(user)
    page = request.META.get('HTTP_REFERER')
    return redirect(page)


class Wishlist(ListView):
    model = Product
    template_name = 'shop/wishlist.html'
    context_object_name = 'wishlist_products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Wishlist: {self.request.user.first_name}'
        return context

    def get_queryset(self):
        return Product.objects.filter(users_wishlist=self.request.user.id)

def add_to_cart(request, pk):
    user = request.user.id
    product = Product.objects.get(pk=pk)
    if product.users_cart.filter(id=user).exists():
        product.users_cart.remove(user)
    else:
        product.users_cart.add(user)

    page = request.META.get('HTTP_REFERER')
    return redirect(page)

class Cart(ListView):
    model = Product
    template_name = 'shop/cart.html'
    context_object_name = 'cart_products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_products'] = Product.objects.filter(users_wishlist=self.request.user.id)
        context['title'] = f'Cart: {self.request.user.first_name}'
        return context

    def get_queryset(self):
        return Product.objects.filter(users_cart=self.request.user.id)

def remove_from_cart(request, pk):
    user = request.user.id
    product = Product.objects.get(pk=pk)
    product.users_cart.remove(user)
    page = request.META.get('HTTP_REFERER')
    return redirect(page)

def submit_comment(request, pk):
    product_comment = Product.objects.get(pk=pk).pk
    user = request.user.id
    content = request.POST.get('content')
    Comments.objects.create(user_posted_id=user, product_of_comment_id=product_comment, content=content)
    page = request.META.get('HTTP_REFERER')
    return redirect(page)

def order(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product_price = int(product.price)
        quantity = int(request.POST.get('product_quantity'))
        shipping_cost = 2 * quantity
        sub_total = product_price * quantity
        grand_total = sub_total + shipping_cost
        form = MakeOrderForm(request.POST)
        if form.is_valid():
            form.instance.product_id = product.id
            form.instance.shipping_cost = shipping_cost
            form.instance.grand_total = grand_total
            form.instance.user_made_order_id = request.user.id
            form.save()
            messages.success(request, 'Order made successfully!')
            send_mail(f"Dear, {request.user.username}", f'Thank you for ordering {product.name}... some more text ',
                             'couldzet@gmail.com', [form.cleaned_data['email']])
            return redirect('home')
        else:
            print(form.errors.as_data())
    else:
        form = MakeOrderForm
    return render(request, 'shop/checkout.html', {'form': form, 'product': product, 'title': f'{request.user.username}: Make order'})
