from django.contrib import admin

from .models import Category,Product,Review

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","dt"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","dt","release_date","category"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["comment","dt","spoiler","product"]

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Review,ReviewAdmin)
