from django.db import models
from manage import init_django
init_django()


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)


class Good(Model):
    title = models.CharField(max_length=512, blank=False, db_index=True)
    href = models.CharField(max_length=255, blank=False, unique=True)
    price = models.CharField(max_length=128, blank=False)
    prefix = models.CharField(max_length=128, blank=False)
    category = models.ForeignKey(Category, blank=False, on_delete=models.CASCADE)
    
    wheight = models.IntegerField(blank=True, default=0)
    coef = models.FloatField(blank=True, default=0)