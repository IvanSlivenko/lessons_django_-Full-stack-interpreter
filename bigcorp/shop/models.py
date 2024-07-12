import random
import string
from django.db import models
from django.utils.text import slugify
from django.urls import reverse



class Category(models.Model):

    
    name = models.CharField("Категорія",max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null= True
    )
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)
    created_ad = models.DateTimeField('Дата створення', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категорія' 
        verbose_name_plural = 'Категорії'

    def __str__(self) -> str:
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])
    def _rand_slug():
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


    def save(self, *args, **kwargs):
          if  not self.slug:
              self.slug = slugify(self._rand_slug() +'-pickBetter' + self.name)
          super(Category, self.save(*args, **kwargs))     

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})

class  Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField("Назва", max_length=250)
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Опис", blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Ціна', max_digits=7, decimal_places=2, default=99.99)
    image =  models.ImageField('Зображення', upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField('Наявність', default=True)
    created_ad = models.DateTimeField('Дата створення', auto_now_add=True)
    updated_at = models.DateTimeField('Дата редагування', auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'

    def __str__(self) -> str:
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})

class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(ProductManager, self).get_queryset().filter(available=True)

class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True






