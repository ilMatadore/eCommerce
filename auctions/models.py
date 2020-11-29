from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='product_category')
    image = models.ImageField(upload_to='images', blank=True, null=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_created_listing')
    closed = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    bids = models.ManyToManyField(
        'Bid', related_name='bids_in_the_product', blank=True)
    last_bid = models.ForeignKey('Bid', on_delete=models.CASCADE,
                                 related_name='last_bid_for_the_auction', blank=True, null=True)
    lastBid = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_watchlist')
    product = models.ManyToManyField(
        'Product', related_name='products_in_the_watchlist', blank=True)

    def __str__(self):
        return f"{self.user}"


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_commented')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_commented')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.comment} in {self.product} by {self.user}"


class Bid(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='user_placed_bid')
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_bid')
    bid = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.bid)
