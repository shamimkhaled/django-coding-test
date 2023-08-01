from django.contrib import admin
from .models import *

# Register your models here.
myModels = [Variant, Product, ProductVariant, ProductVariantPrice]
admin.site.register(myModels)