from django.contrib import admin
from django.contrib.admin import ModelAdmin
from sastakart.models import *
from django_mptt_admin.admin import DjangoMpttAdmin

class ListingAdmin(ModelAdmin):
	list_display=['id','store','price','product']

class ProductAdmin(ModelAdmin):
	list_display=['id','title','category','msp_id']


class CategoryAdmin(DjangoMpttAdmin):
	list_display=['name','parent']	

class ReviewAdmin(ModelAdmin):
	list_display=['id','listing']	

admin.site.register
admin.site.register(Product,ProductAdmin)
admin.site.register(Listing,ListingAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Review,ReviewAdmin)