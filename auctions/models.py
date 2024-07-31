from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bid}"
    

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing_bid")
    image_url = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")


class Comment(models.Model):
    content = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")

    def __str__(self):
        return f"{self.user} comment on {self.listing}"