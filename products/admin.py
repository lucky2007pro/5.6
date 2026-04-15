from django.contrib import admin
from .models import Product, ProductImage, Category, Comment, Saved, Like, RecentlyProduct, ProductView

admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ["id","category","price"]
    list_filter = ["category", 'discount']
    search_fields = ["title","desc"]
    pass


admin.site.register(Comment)
admin.site.register(Saved)
admin.site.register(Like)
admin.site.register(RecentlyProduct)
admin.site.register(ProductView)

