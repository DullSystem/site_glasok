from django.db import models
from main.models import Product


class Order(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия",max_length=50)
    email = models.EmailField()
    address = models.CharField("Адрес", max_length=250)
    postal_code = models.CharField("Почтовый Код", max_length=20)
    city = models.CharField("Город", max_length=100)
    created = models.DateTimeField("Созданный", auto_now_add=True)
    updated = models.DateTimeField("Обновлен", auto_now=True)
    paid = models.BooleanField("Оплаченный", default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


def __str__(self):
    return 'Order {}'.format(self.id)


def get_total_cost(self):
    return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='order_items')
    price = models.CharField("Цена", max_length=200, db_index=True, blank=True)
    quantity = models.PositiveIntegerField("Количество", default=1)
    size = models.CharField("Оптическая сила", max_length=200, db_index=True, blank=True)

    def __str__(self):
        return '{}'.format(self.id)


def get_cost(self):
    return self.price * self.quantity
