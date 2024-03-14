from django.contrib import admin
from .models import Transaction, AppUser, Category

# Register your models here.
admin.site.register(Transaction)
admin.site.register(AppUser)
admin.site.register(Category)