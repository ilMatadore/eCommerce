from django.contrib import admin
from .models import Category, Product, User, Watchlist, Comment, Bid


# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)
