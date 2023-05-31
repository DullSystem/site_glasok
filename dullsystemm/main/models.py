from django.db import models
from django.urls import reverse

from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class Prices(models.Model):  # Для цен на услуги врача
    price_title = models.CharField('Наименование услуги', max_length=200)
    price_text = models.TextField('Описание услуги')

    objects = models.Manager()

    def __str__(self):
        return self.price_title

    class Meta:
        verbose_name = 'Наименование услуги (врача)'
        verbose_name_plural = 'Наименование услуг (врача)'


class Doctor(models.Model):  # Показываем информацию о враче
    Doctor_visit = models.CharField('Наименование', max_length=200)
    Doctor_text = models.TextField('Описание услуги', blank=True)
    Doctor_text1 = models.TextField('Описание услуги', blank=True)
    Doctor_text2 = models.TextField('Описание услуги', blank=True)
    Doctor_text3 = models.TextField('Описание услуги', blank=True)
    Doctor_text4 = models.TextField('Описание услуги', blank=True)
    Doctor_text5 = models.TextField('Описание услуги', blank=True)
    Doctor_text6 = models.TextField('Описание услуги', blank=True)
    image = models.ImageField("Фото врача", upload_to='gallery', blank=True)
    image1 = models.ImageField("Фото врача", upload_to='gallery', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.Doctor_visit

    class Meta:
        verbose_name = 'Информация о враче'
        verbose_name_plural = 'Информация о врачах'


class Category(models.Model):  # На товары и аксессуары глаза
    name = models.CharField('Наименование', max_length=200, db_index=True)
    slug = models.SlugField('Описание', max_length=200, db_index=True, unique=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name


class Product(models.Model):
    lenses = 'lenses'
    Accessories = 'Accessories'
    solutions = 'solutions'
    glasses = 'glasses'

    GROUP_CATEGORY = {
        (lenses, 'lenses'),
        (Accessories, 'Accessories'),
        (solutions, 'solutions'),
        (glasses, 'glasses'), }  # Для выбора категории, чтобы потом показать нужный товар

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    url_slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    name = models.CharField("Наименование", max_length=200, db_index=True)
    slug = models.CharField("Плановая замена", max_length=200, db_index=True, blank=True)
    description = models.TextField("Описание", blank=True)
    optical = models.DecimalField("Оптическая сила", max_digits=10, decimal_places=2, blank=True, null=True)
    radius = models.DecimalField("Радиус кривизны", max_digits=10, decimal_places=1, blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("В наличии:")
    available = models.BooleanField("Доступен ли продукт", default=True)
    created = models.DateTimeField("Дата создания объекта", auto_now_add=True)
    updated = models.DateTimeField("Время последнего обновления", auto_now=True)
    group = models.CharField("Категория", choices=GROUP_CATEGORY, max_length=200, db_index=True)
    pubdate = models.DateTimeField("Годен до:", default=timezone.now, blank=True, null=True)
    id = models.AutoField('№', primary_key=True)
    image = models.ImageField("Вид товара", upload_to='gallery')
    image1 = models.ImageField("Развёрнутый вид товара", upload_to='gallery')
    objects = models.Manager()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return f'/{self.url_slug}/'  # Для перехода к определенному товару
        return reverse('product_detail', args=[self.id, self.url_slug])



class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['product_id']

    def __str__(self):
        return f'{self.product.name}'


# Отзывы
class Post_user(models.Model):
    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='blog_posts')
    date_added = models.DateTimeField("Дата создания", auto_now_add=True)
    slug = models.SlugField(max_length=200, null=False, unique=True, verbose_name='URL')
    title = models.CharField("Наименование", max_length=200, unique=True)
    content = models.TextField("Информация")

    class Meta:
        ordering = ["date_added"]

        verbose_name = 'Пост для комментариев'
        verbose_name_plural = 'Пост для комментария'

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", kwargs={"slug": str(self.slug)})


class Comments_User(models.Model):
    user = models.ForeignKey(Post_user, default=1, on_delete=models.SET_DEFAULT, related_name='comments')
    author_name = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='user')
    username = models.CharField("Наименование", max_length=80, blank=True)

    body = models.TextField("Отзыв")
    created_on = models.DateTimeField("Время создания", auto_now_add=True)
    active = models.BooleanField("Активен", default=False)

    class Meta:
        ordering = ['created_on']

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)


# Новостная лента
class Post_news(models.Model):
    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='posts')
    date_added = models.DateTimeField("Дата создания", auto_now_add=True)
    slug = models.SlugField(max_length=200, null=False, unique=True, verbose_name='URL')
    title = models.CharField("Наименование", max_length=200, unique=True)
    content = models.TextField("Информация")
    post_image = models.ImageField("Изображение", upload_to='gallery', blank=True)

    class Meta:
        ordering = ["date_added"]

        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("news", kwargs={"slug": str(self.slug)})



class Comments_news(models.Model):
    post = models.ForeignKey(Post_news, default=1, on_delete=models.SET_DEFAULT, related_name='news_comments')
    author_news = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='author')
    username = models.CharField("Наименование", max_length=80, blank=True)

    body = models.TextField("Комментарий")
    created_on = models.DateTimeField("Время создания", auto_now_add=True)
    active = models.BooleanField("Активен", default=False)

    class Meta:
        ordering = ['created_on']

        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)

