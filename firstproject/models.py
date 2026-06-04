from django.db import models
from django.conf import settings
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Название", max_length=120)
    slug = models.SlugField("Слаг", unique=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("firstproject:category_detail", kwargs={"slug": self.slug})


class Club(models.Model):
    name = models.CharField("Клуб", max_length=120)
    country = models.CharField("Страна", max_length=80)
    league = models.CharField("Лига", max_length=120)
    logo = models.CharField("Фото/логотип", max_length=180, blank=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Футбольный клуб"
        verbose_name_plural = "Футбольные клубы"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("firstproject:club_detail", kwargs={"pk": self.pk})


class Brand(models.Model):
    name = models.CharField("Бренд", max_length=120)
    country = models.CharField("Страна", max_length=80)
    logo = models.CharField("Фото/логотип", max_length=180, blank=True)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("firstproject:brand_detail", kwargs={"pk": self.pk})


class Supplier(models.Model):
    name = models.CharField("Поставщик", max_length=140)
    city = models.CharField("Город", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=30)
    description = models.TextField("Описание")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("firstproject:supplier_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField("Товар", max_length=160)
    slug = models.SlugField("Слаг", unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Клуб",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Бренд",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Поставщик",
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Остаток")
    photo = models.CharField("Фото", max_length=180, blank=True)
    short_description = models.CharField("Краткое описание", max_length=240)
    description = models.TextField("Подробное описание")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("firstproject:product_detail", kwargs={"slug": self.slug})


class Customer(models.Model):
    first_name = models.CharField("Имя", max_length=80)
    last_name = models.CharField("Фамилия", max_length=80)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=30)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Order(models.Model):
    STATUS_NEW = "new"
    STATUS_PAID = "paid"
    STATUS_SENT = "sent"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новый"),
        (STATUS_PAID, "Оплачен"),
        (STATUS_SENT, "Отправлен"),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Покупатель",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Пользователь",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Дата заказа", auto_now_add=True)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW
    )
    delivery_address = models.CharField("Адрес доставки", max_length=240)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk}"

    def get_absolute_url(self):
        return reverse("firstproject:order_detail", kwargs={"pk": self.pk})

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField("Количество")
    price = models.DecimalField("Цена на момент заказа", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price
