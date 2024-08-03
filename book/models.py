from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField
from django.utils.text import slugify


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="groups/", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    discount = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.zero.value)
    image = models.ImageField(upload_to='products/')
    slug = models.SlugField(unique=True, blank=True)
    on_sale = models.BooleanField(default=False)
    user_like = ManyToManyField(User, related_name='liked_products', blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='products')

    @property
    def discounted_price(self):
        if self.discount > 0:
            return round(self.price * (1 - self.discount / 100), 2)
        else:
            return self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)


class Comment(models.Model):
    rating = models.CharField(max_length=10)
    message = models.TextField()
    file = models.FileField(upload_to="comments/")
    product_fk = models.ForeignKey(Product, on_delete=models.CASCADE)
