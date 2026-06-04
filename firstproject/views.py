from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

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
from .cart import Cart
from .models import Brand, Category, Club, Customer, Order, OrderItem, Product, Supplier

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для выполнения этого действия.")
        return redirect("firstproject:home")


class FormContextMixin:
    action_label = "Сохранить"
    cancel_url_name = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_label"] = self.action_label
        if self.cancel_url_name:
            context["cancel_url"] = reverse_lazy(self.cancel_url_name)
        return context


class DeleteContextMixin:
    cancel_url_name = None
    object_label = "объект"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_label"] = self.object_label
        if self.cancel_url_name:
            context["cancel_url"] = reverse_lazy(self.cancel_url_name)
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                "Запись нельзя удалить, потому что она используется в связанных данных.",
            )
            return redirect(self.get_success_url())


class HomeView(TemplateView):
    template_name = "firstproject/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_products"] = Product.objects.select_related(
            "category", "club", "brand"
        )[:4]
        return context


class AboutView(TemplateView):
    template_name = "firstproject/about.html"


class CartView(TemplateView):
    template_name = "firstproject/cart.html"

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
        return redirect("firstproject:cart")


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
        return redirect("firstproject:cart")


class RemoveFromCartView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart = Cart(request)
        cart.remove(product)
        messages.success(request, "Товар удален из корзины.")
        return redirect("firstproject:cart")


class CreateOrderFromCartView(LoginRequiredMixin, View):
    login_url = reverse_lazy("firstproject:login")

    def post(self, request):
        cart = Cart(request)
        items = list(cart)
        if not items:
            messages.error(request, "Корзина пуста, заказ не создан.")
            return redirect("firstproject:cart")
        form = OrderCreateForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Укажите адрес доставки.")
            return redirect("firstproject:cart")

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


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("firstproject:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация выполнена. Вы вошли в аккаунт.")
        return response


class ProductListView(ListView):
    model = Product
    template_name = "firstproject/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("category", "club", "brand", "supplier")


class ProductDetailView(DetailView):
    model = Product
    template_name = "firstproject/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Product.objects.select_related("category", "club", "brand", "supplier")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context


class ProductCreateView(StaffRequiredMixin, FormContextMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить товар"
    cancel_url_name = "firstproject:product_list"


class ProductUpdateView(StaffRequiredMixin, FormContextMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "firstproject/entity_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    action_label = "Сохранить товар"
    cancel_url_name = "firstproject:product_list"


class ProductDeleteView(StaffRequiredMixin, DeleteContextMixin, DeleteView):
    model = Product
    template_name = "firstproject/entity_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("firstproject:product_list")
    cancel_url_name = "firstproject:product_list"
    object_label = "товар"


class CategoryListView(ListView):
    model = Category
    template_name = "firstproject/category_list.html"
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "firstproject/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class CategoryCreateView(StaffRequiredMixin, FormContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить категорию"
    cancel_url_name = "firstproject:category_list"


class CategoryUpdateView(StaffRequiredMixin, FormContextMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "firstproject/entity_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    action_label = "Сохранить категорию"
    cancel_url_name = "firstproject:category_list"


class CategoryDeleteView(StaffRequiredMixin, DeleteContextMixin, DeleteView):
    model = Category
    template_name = "firstproject/entity_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("firstproject:category_list")
    cancel_url_name = "firstproject:category_list"
    object_label = "категорию"


class ClubListView(ListView):
    model = Club
    template_name = "firstproject/club_list.html"
    context_object_name = "clubs"


class ClubDetailView(DetailView):
    model = Club
    template_name = "firstproject/club_detail.html"
    context_object_name = "club"


class ClubCreateView(StaffRequiredMixin, FormContextMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить клуб"
    cancel_url_name = "firstproject:club_list"


class ClubUpdateView(StaffRequiredMixin, FormContextMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = "firstproject/entity_form.html"
    action_label = "Сохранить клуб"
    cancel_url_name = "firstproject:club_list"


class ClubDeleteView(StaffRequiredMixin, DeleteContextMixin, DeleteView):
    model = Club
    template_name = "firstproject/entity_confirm_delete.html"
    success_url = reverse_lazy("firstproject:club_list")
    cancel_url_name = "firstproject:club_list"
    object_label = "клуб"


class BrandListView(ListView):
    model = Brand
    template_name = "firstproject/brand_list.html"
    context_object_name = "brands"


class BrandDetailView(DetailView):
    model = Brand
    template_name = "firstproject/brand_detail.html"
    context_object_name = "brand"


class BrandCreateView(StaffRequiredMixin, FormContextMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить бренд"
    cancel_url_name = "firstproject:brand_list"


class BrandUpdateView(StaffRequiredMixin, FormContextMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "firstproject/entity_form.html"
    action_label = "Сохранить бренд"
    cancel_url_name = "firstproject:brand_list"


class BrandDeleteView(StaffRequiredMixin, DeleteContextMixin, DeleteView):
    model = Brand
    template_name = "firstproject/entity_confirm_delete.html"
    success_url = reverse_lazy("firstproject:brand_list")
    cancel_url_name = "firstproject:brand_list"
    object_label = "бренд"


class SupplierListView(ListView):
    model = Supplier
    template_name = "firstproject/supplier_list.html"
    context_object_name = "suppliers"


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = "firstproject/supplier_detail.html"
    context_object_name = "supplier"


class SupplierCreateView(StaffRequiredMixin, FormContextMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить поставщика"
    cancel_url_name = "firstproject:supplier_list"


class SupplierUpdateView(StaffRequiredMixin, FormContextMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "firstproject/entity_form.html"
    action_label = "Сохранить поставщика"
    cancel_url_name = "firstproject:supplier_list"


class SupplierDeleteView(StaffRequiredMixin, DeleteContextMixin, DeleteView):
    model = Supplier
    template_name = "firstproject/entity_confirm_delete.html"
    success_url = reverse_lazy("firstproject:supplier_list")
    cancel_url_name = "firstproject:supplier_list"
    object_label = "поставщика"


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "firstproject/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        queryset = Order.objects.select_related("customer", "user").prefetch_related(
            "items"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "firstproject/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        queryset = Order.objects.select_related("customer", "user").prefetch_related(
            "items__product"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
