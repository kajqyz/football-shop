from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Brand, Category, Club, Product, Supplier


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class StyledModelForm(forms.ModelForm):
    textarea_rows = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("rows", self.textarea_rows)


class CategoryForm(StyledModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description"]


class ClubForm(StyledModelForm):
    class Meta:
        model = Club
        fields = ["name", "country", "league", "logo", "description"]


class BrandForm(StyledModelForm):
    class Meta:
        model = Brand
        fields = ["name", "country", "logo", "description"]


class SupplierForm(StyledModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "city", "email", "phone", "description"]


class ProductForm(StyledModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "category",
            "club",
            "brand",
            "supplier",
            "price",
            "stock",
            "photo",
            "short_description",
            "description",
        ]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label="Количество",
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
    )
    reload = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["quantity"].widget.attrs["class"] = "quantity-input"


class OrderCreateForm(forms.Form):
    delivery_address = forms.CharField(
        label="Адрес доставки",
        max_length=240,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите адрес доставки",
            }
        ),
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Имя", max_length=80, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=80, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
