from rest_framework.routers import DefaultRouter

from shop_api.views import (
    BrandViewSet,
    CategoryViewSet,
    ClubViewSet,
    CustomerViewSet,
    OrderItemViewSet,
    OrderViewSet,
    ProductViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="api-category")
router.register("clubs", ClubViewSet, basename="api-club")
router.register("brands", BrandViewSet, basename="api-brand")
router.register("suppliers", SupplierViewSet, basename="api-supplier")
router.register("products", ProductViewSet, basename="api-product")
router.register("customers", CustomerViewSet, basename="api-customer")
router.register("orders", OrderViewSet, basename="api-order")
router.register("order-items", OrderItemViewSet, basename="api-order-item")

urlpatterns = router.urls
