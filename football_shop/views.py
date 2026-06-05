from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .cart import Cart
from .forms import (
    BrandForm,
    CartAddProductForm,
    CategoryForm,
    ClubForm,
    OrderCreateForm,
    ProductForm,
    RegistrationForm,
    SupplierForm,
)
from .models import Brand, Category, Club, Customer, Order, OrderItem, Product, Supplier


# Проверка для страниц управления данными.
# Пользователь должен быть сотрудником сайта.
staff_required = user_passes_test(
    lambda user: user.is_staff,
    login_url=reverse_lazy("shop:home"),
)


def delete_object_safely(view, form):
    try:
        return super(view.__class__, view).form_valid(form)
    except ProtectedError:
        messages.error(
            view.request,
            "Запись нельзя удалить, потому что она используется в связанных данных.",
        )
        return redirect(view.get_success_url())


# Практическая 2. CRUD-страницы через generic views.

class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category", "club", "brand", "supplier")


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.select_related("category", "club", "brand", "supplier")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context


@method_decorator(staff_required, name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/entity_form.html"
    action_label = "Добавить товар"
    cancel_url_name = "shop:product_list"


@method_decorator(staff_required, name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/entity_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    action_label = "Сохранить товар"
    cancel_url_name = "shop:product_list"


@method_decorator(staff_required, name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "shop/entity_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("shop:product_list")
    cancel_url_name = "shop:product_list"
    object_label = "товар"

    def form_valid(self, form):
        return delete_object_safely(self, form)


class CategoryListView(ListView):
    model = Category
    template_name = "shop/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "shop/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"


@method_decorator(staff_required, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "shop/entity_form.html"
    action_label = "Добавить категорию"
    cancel_url_name = "shop:category_list"


@method_decorator(staff_required, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "shop/entity_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    action_label = "Сохранить категорию"
    cancel_url_name = "shop:category_list"


@method_decorator(staff_required, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "shop/entity_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("shop:category_list")
    cancel_url_name = "shop:category_list"
    object_label = "категорию"

    def form_valid(self, form):
        return delete_object_safely(self, form)


class ClubListView(ListView):
    model = Club
    template_name = "shop/club_list.html"
    context_object_name = "clubs"


class ClubDetailView(DetailView):
    model = Club
    template_name = "shop/club_detail.html"
    context_object_name = "club"


@method_decorator(staff_required, name="dispatch")
class ClubCreateView(CreateView):
    model = Club
    form_class = ClubForm
    template_name = "shop/entity_form.html"
    action_label = "Добавить клуб"
    cancel_url_name = "shop:club_list"


@method_decorator(staff_required, name="dispatch")
class ClubUpdateView(UpdateView):
    model = Club
    form_class = ClubForm
    template_name = "shop/entity_form.html"
    action_label = "Сохранить клуб"
    cancel_url_name = "shop:club_list"


@method_decorator(staff_required, name="dispatch")
class ClubDeleteView(DeleteView):
    model = Club
    template_name = "shop/entity_confirm_delete.html"
    success_url = reverse_lazy("shop:club_list")
    cancel_url_name = "shop:club_list"
    object_label = "клуб"

    def form_valid(self, form):
        return delete_object_safely(self, form)


class BrandListView(ListView):
    model = Brand
    template_name = "shop/brand_list.html"
    context_object_name = "brands"


class BrandDetailView(DetailView):
    model = Brand
    template_name = "shop/brand_detail.html"
    context_object_name = "brand"


@method_decorator(staff_required, name="dispatch")
class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "shop/entity_form.html"
    action_label = "Добавить бренд"
    cancel_url_name = "shop:brand_list"


@method_decorator(staff_required, name="dispatch")
class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "shop/entity_form.html"
    action_label = "Сохранить бренд"
    cancel_url_name = "shop:brand_list"


@method_decorator(staff_required, name="dispatch")
class BrandDeleteView(DeleteView):
    model = Brand
    template_name = "shop/entity_confirm_delete.html"
    success_url = reverse_lazy("shop:brand_list")
    cancel_url_name = "shop:brand_list"
    object_label = "бренд"

    def form_valid(self, form):
        return delete_object_safely(self, form)


class SupplierListView(ListView):
    model = Supplier
    template_name = "shop/supplier_list.html"
    context_object_name = "suppliers"


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = "shop/supplier_detail.html"
    context_object_name = "supplier"


@method_decorator(staff_required, name="dispatch")
class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "shop/entity_form.html"
    action_label = "Добавить поставщика"
    cancel_url_name = "shop:supplier_list"


@method_decorator(staff_required, name="dispatch")
class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "shop/entity_form.html"
    action_label = "Сохранить поставщика"
    cancel_url_name = "shop:supplier_list"


@method_decorator(staff_required, name="dispatch")
class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = "shop/entity_confirm_delete.html"
    success_url = reverse_lazy("shop:supplier_list")
    cancel_url_name = "shop:supplier_list"
    object_label = "поставщика"

    def form_valid(self, form):
        return delete_object_safely(self, form)


# Следующие практические. Главная страница, регистрация, корзина, заказы.

class HomeView(TemplateView):
    template_name = "shop/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = Product.objects.select_related(
            "category", "club", "brand"
        )[:4]
        return context


class AboutView(TemplateView):
    template_name = "shop/about.html"


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("shop:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация выполнена. Вы вошли в аккаунт.")
        return response


class CartView(TemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context["cart"] = cart
        context["cart_items"] = list(cart)
        context["cart_total_price"] = cart.get_total_price()
        context["cart_total_quantity"] = len(cart)
        context["order_form"] = OrderCreateForm()
        return context


class AddToCartView(View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if product.stock <= 0:
            messages.error(request, "Товара нет в наличии.")
            return redirect(product.get_absolute_url())
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            cart.add(
                product=product,
                quantity=form.cleaned_data["quantity"],
                reload=form.cleaned_data["reload"],
            )
            messages.success(request, f"Товар «{product.name}» добавлен в корзину.")
        return redirect("shop:cart")


class UpdateCartItemView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cart = Cart(request)
            cart.add(
                product=product,
                quantity=form.cleaned_data["quantity"],
                reload=True,
            )
            messages.success(request, "Количество товара обновлено.")
        return redirect("shop:cart")


class RemoveFromCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.remove(product)
        messages.success(request, "Товар удален из корзины.")
        return redirect("shop:cart")


@method_decorator(login_required(login_url=reverse_lazy("shop:login")), name="dispatch")
class CreateOrderFromCartView(View):
    def post(self, request):
        cart = Cart(request)
        items = list(cart)
        if not items:
            messages.error(request, "Корзина пуста, заказ не создан.")
            return redirect("shop:cart")
        form = OrderCreateForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Укажите адрес доставки.")
            return redirect("shop:cart")

        customer, _created = Customer.objects.get_or_create(
            email=request.user.email,
            defaults={
                "first_name": request.user.first_name or request.user.username,
                "last_name": request.user.last_name or "Покупатель",
                "phone": "",
            },
        )
        order = Order.objects.create(
            customer=customer,
            user=request.user,
            delivery_address=form.cleaned_data["delivery_address"],
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        cart.clear()
        messages.success(request, f"Заказ #{order.id} создан.")
        return redirect(order.get_absolute_url())


@method_decorator(login_required(login_url=reverse_lazy("shop:login")), name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "shop/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.select_related("customer", "user").prefetch_related(
            "items"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


@method_decorator(login_required(login_url=reverse_lazy("shop:login")), name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "shop/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        queryset = Order.objects.select_related("customer", "user").prefetch_related(
            "items__product"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
