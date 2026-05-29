from django import forms

from .models import Brand, Category, Club, Product, Supplier


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
