from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название продукта')
    slug = models.CharField(max_length=250, unique=True, verbose_name='Slug')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Фото')
    image2 = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Фото 2', blank=True)
    image3 = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Фото 3', blank=True)
    image4 = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Фото 4', blank=True)
    description = models.TextField(verbose_name='Описание')
    specification = models.TextField(verbose_name='Спецификация')
    color = models.ManyToManyField('ProductColor', verbose_name='Цвет')
    size = models.ManyToManyField('ProductSize', verbose_name='Размер', blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    featured = models.BooleanField(default=False)
    brand = models.ForeignKey('Brands', on_delete=models.PROTECT, verbose_name='Бренд')
    users_wishlist = models.ManyToManyField('Account', related_name='user_wishlist', blank=True)
    users_cart = models.ManyToManyField('Account', related_name='user_cart', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"slug": self.slug})

class ProductColor(models.Model):
    color_name = models.CharField(max_length=150, verbose_name='Цвет')
    slug = models.CharField(max_length=250, unique=True, verbose_name='Slug')

    def __str__(self):
        return self.color_name

class ProductSize(models.Model):
    size_name = models.CharField(max_length=150, verbose_name='Размер')
    slug = models.CharField(max_length=250, unique=True, verbose_name='Slug')

    def __str__(self):
        return self.size_name

class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название категории')
    slug = models.CharField(max_length=250, unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='images/%Y/%m%d', verbose_name='Фото категории', blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class UserEmails(models.Model):
    email = models.CharField(max_length=250, verbose_name='email', unique=True)


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, mobile, password=None):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not mobile:
            raise ValueError("Phone number is required")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, mobile, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            mobile=mobile,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def refresh_from_db(self, using=None, fields=None, **kwargs):
        # fields contains the name of the deferred field to be
        # loaded.
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            # If any deferred field is going to be loaded
            if fields.intersection(deferred_fields):
                # then load all of them
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

class Account(AbstractUser):
    email = models.EmailField(max_length=200, verbose_name='email', unique=True)
    username = models.CharField(max_length=200, verbose_name='username', unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last login')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    mobile = models.CharField(max_length=30, verbose_name='Phone number', unique=True)
    address = models.CharField(max_length=150, verbose_name='Address')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile', 'first_name']

    objects = MyAccountManager()

    def get_absolute_url(self):
        return reverse("profile", kwargs={'pk': self.pk})

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class Brands(models.Model):
    slug = models.CharField(max_length=200, verbose_name='Slug', unique=True)
    title = models.CharField(max_length=200, verbose_name='Название бренда')

    def get_absolute_url(self):
        return reverse('brand', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Comments(models.Model):
    user_posted = models.ForeignKey(Account, related_name='user_comment', verbose_name='Имя пользователя', on_delete=models.CASCADE)
    product_of_comment = models.ForeignKey(Product, related_name='product_comment', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


class Order(models.Model):
    STATUS_CHOISES = [
        ('IN PROCESSING', 'In processing'),
        ('DELIVERING', 'Delivering'),
        ('DELIVERED', 'Delivered'),
        ('TAKEN FROM MAIL', 'Taken from mail')
    ]

    PAYMENT_METHOD_CHOISES = [
        ('PAYPAL', 'Paypal'),
        ('PAYONEER', 'Payoneer'),
        ('CHECK PAYMENT', 'Check Payment'),
        ('DIRECT BANK TRANSFER', 'Direct Bank Transfer'),
        ('CASH ON DELIVERY', 'Cash on Delivery')
    ]

    user_made_order = models.ForeignKey(Account, related_name='user_orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOISES, default='IN PROCESSING', max_length=35, verbose_name='Статус заказа')
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOISES, default='PAYPAL', max_length=50, verbose_name='Метод оплаты')
    product_quantity = models.IntegerField(default=1, verbose_name='Количество товара')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Имя')
    mobile = models.CharField(max_length=30, verbose_name='Phone number')
    email = models.EmailField(max_length=150, verbose_name='email')
    address = models.CharField(max_length=150, verbose_name='Адрес')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    state = models.CharField(max_length=100, verbose_name='Штат', blank=True)
    zip_code = models.IntegerField(verbose_name='Zip Code')
    shipping_cost = models.CharField(max_length=150, verbose_name='Цена доставки')
    grand_total = models.CharField(max_length=150, verbose_name='Сумма заказа')
    product = models.ForeignKey(Product, verbose_name='Название товара', on_delete=models.CASCADE)
    #size = models.CharField(choices=Product.size, verbose_name='Размер')
    #color = models.CharField(choices=Product.color, verbose_name='Цвет')


