from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Debate(models.Model):
    title = models.CharField(max_length=255, verbose_name= "Зоголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name= "Зоголовок")
    image = models.ImageField(upload_to="image/%Y/%m/%d/", verbose_name= "Зоголовок")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name= "Зоголовок")
    time_update = models.DateTimeField(auto_now=True, verbose_name= "Зоголовок")
    is_published = models.BooleanField(default=True, verbose_name= "Зоголовок")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name= "Категории")
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('debate', kwargs={'page_slug': self.slug})

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Categories")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Categories"
        verbose_name_plural = "Categories"
        ordering = ['id']