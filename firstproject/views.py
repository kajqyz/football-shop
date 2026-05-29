from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import BrandForm, CategoryForm, ClubForm, ProductForm, SupplierForm
from .models import Brand, Category, Club, Order, Product, Supplier


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


class ProductCreateView(FormContextMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить товар"
    cancel_url_name = "firstproject:product_list"


class ProductUpdateView(FormContextMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "firstproject/entity_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    action_label = "Сохранить товар"
    cancel_url_name = "firstproject:product_list"


class ProductDeleteView(DeleteContextMixin, DeleteView):
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


class CategoryCreateView(FormContextMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить категорию"
    cancel_url_name = "firstproject:category_list"


class CategoryUpdateView(FormContextMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "firstproject/entity_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    action_label = "Сохранить категорию"
    cancel_url_name = "firstproject:category_list"


class CategoryDeleteView(DeleteContextMixin, DeleteView):
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


class ClubCreateView(FormContextMixin, CreateView):
    model = Club
    form_class = ClubForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить клуб"
    cancel_url_name = "firstproject:club_list"


class ClubUpdateView(FormContextMixin, UpdateView):
    model = Club
    form_class = ClubForm
    template_name = "firstproject/entity_form.html"
    action_label = "Сохранить клуб"
    cancel_url_name = "firstproject:club_list"


class ClubDeleteView(DeleteContextMixin, DeleteView):
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


class BrandCreateView(FormContextMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить бренд"
    cancel_url_name = "firstproject:brand_list"


class BrandUpdateView(FormContextMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "firstproject/entity_form.html"
    action_label = "Сохранить бренд"
    cancel_url_name = "firstproject:brand_list"


class BrandDeleteView(DeleteContextMixin, DeleteView):
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


class SupplierCreateView(FormContextMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "firstproject/entity_form.html"
    action_label = "Добавить поставщика"
    cancel_url_name = "firstproject:supplier_list"


class SupplierUpdateView(FormContextMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "firstproject/entity_form.html"
    action_label = "Сохранить поставщика"
    cancel_url_name = "firstproject:supplier_list"


class SupplierDeleteView(DeleteContextMixin, DeleteView):
    model = Supplier
    template_name = "firstproject/entity_confirm_delete.html"
    success_url = reverse_lazy("firstproject:supplier_list")
    cancel_url_name = "firstproject:supplier_list"
    object_label = "поставщика"


class OrderListView(ListView):
    model = Order
    template_name = "firstproject/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.select_related("customer").prefetch_related("items")


class OrderDetailView(DetailView):
    model = Order
    template_name = "firstproject/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.select_related("customer").prefetch_related(
            "items__product"
        )
