from django.contrib import admin
from django.urls import path
from marketplace import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
path("farmer-register/", views.farmer_register, name="farmer_register"),
path("customer-register/", views.customer_register, name="customer_register"),
path("login/", views.login_page, name="login"),

path("farmer-dashboard/", views.farmer_dashboard, name="farmer_dashboard"),
path("add-product/", views.add_product, name="add_product"),
    path("my-products/", views.my_products, name="my_products"),
path("customer-products/", views.customer_products, name="customer_products"),
path(
    "buy-product/<int:product_id>/",
    views.buy_product,
    name="buy_product"
),
path("customer-orders/", views.customer_orders, name="customer_orders"),
path("farmer-orders/", views.farmer_orders, name="farmer_orders"),
path("my-products/", views.my_products, name="my_products"),
]