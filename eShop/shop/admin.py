from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms



# Register your models here.

class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    specification = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'price', 'category', 'brand', 'featured')
    list_display_links = ('slug', 'name')
    fields = ('name', 'slug', 'image', 'image2', 'image3', 'image4', 'get_image', 'get_image2', 'get_image3', 'get_image4', 'price', 'description', 'specification', 'category', 'brand', 'color', 'size', 'featured')
    readonly_fields = ('get_image', 'get_image2', 'get_image3', 'get_image4', 'created_at')


    def get_image(self, obj):
        if obj.image:
            return mark_safe((f'<img src="{obj.image.url}">'))

    def get_image2(self, obj):
        if obj.image2:
            return mark_safe((f'<img src="{obj.image2.url}">'))

    def get_image3(self, obj):
        if obj.image3:
            return mark_safe((f'<img src="{obj.image3.url}">'))

    def get_image4(self, obj):
        if obj.image4:
            return mark_safe((f'<img src="{obj.image4.url}">'))

class ProductColorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("color_name",)}
    list_display = ('color_name', 'slug')
    list_display_links = ('color_name', 'slug')

class ProductSizeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("size_name",)}
    list_display = ('size_name', 'slug')
    list_display_links = ('size_name', 'slug')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title')
    list_display_links = ('slug', 'title')
    fields = ('title', 'slug', 'image', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe((f'<img src="{obj.image.url}">'))

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title',)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superuser', 'first_name', 'last_name', 'mobile', 'address')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user_posted', 'product_of_comment', 'content')
    readonly_fields = ('created_at',)

class OrderAdmin(admin.ModelAdmin):
    fields = ('user_made_order', 'product', 'first_name', 'last_name', 'mobile', 'email', 'address', 'country', 'city', 'state', 'zip_code', 'shipping_cost', 'grand_total', 'created_at', 'status', 'payment_method', 'product_quantity')
    list_display = ('user_made_order', 'product', 'first_name', 'last_name', 'mobile', 'email', 'address', 'country', 'city', 'state', 'zip_code', 'shipping_cost', 'grand_total', 'status', 'payment_method', 'product_quantity')
    readonly_fields = ('created_at',)

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brands, BrandAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Order, OrderAdmin)
