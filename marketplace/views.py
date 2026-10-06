from django.shortcuts import render, redirect, get_object_or_404
from .models import Farmer, Customer, Product, Order


# ---------------- HOME ----------------

def home(request):
    return render(request, "marketplace/home.html")


# ---------------- FARMER REGISTER ----------------

def farmer_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        Farmer.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone
        )

        return redirect("login")

    return render(
        request,
        "marketplace/farmer_register.html"
    )


# ---------------- CUSTOMER REGISTER ----------------

def customer_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        Customer.objects.create(
            name=name,
            email=email,
            password=password,
            phone=phone
        )

        return redirect("login")

    return render(
        request,
        "marketplace/customer_register.html"
    )


# ---------------- LOGIN ----------------

def login_page(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check Farmer
        farmer = Farmer.objects.filter(
            email=email,
            password=password
        ).first()

        if farmer:
            request.session["farmer_id"] = farmer.id
            return redirect("farmer_dashboard")

        # Check Customer
        customer = Customer.objects.filter(
            email=email,
            password=password
        ).first()

        if customer:
            request.session["customer_id"] = customer.id
            return redirect("customer_products")

        return render(
            request,
            "marketplace/login.html",
            {
                "error": "Invalid email or password"
            }
        )

    return render(
        request,
        "marketplace/login.html"
    )


# ---------------- FARMER DASHBOARD ----------------

def farmer_dashboard(request):

    farmer_id = request.session.get("farmer_id")

    if not farmer_id:
        return redirect("login")

    farmer = get_object_or_404(
        Farmer,
        id=farmer_id
    )

    return render(
        request,
        "marketplace/farmer_dashboard.html",
        {
            "farmer": farmer
        }
    )

# ---------------- ADD PRODUCT ----------------

def add_product(request):

    farmer_id = request.session.get("farmer_id")

    if not farmer_id:
        return redirect("login")

    farmer = get_object_or_404(
        Farmer,
        id=farmer_id
    )

    if request.method == "POST":

        product_name = request.POST.get("product_name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        Product.objects.create(
            product_name=product_name,
            category=category,
            price=price,
            quantity=quantity,
            farmer=farmer
        )

        return redirect("my_products")

    return render(
        request,
        "marketplace/add_product.html"
    )


# ---------------- MY PRODUCTS ----------------

def my_products(request):

    farmer_id = request.session.get("farmer_id")

    if not farmer_id:
        return redirect("login")

    farmer = get_object_or_404(
        Farmer,
        id=farmer_id
    )

    products = Product.objects.filter(
        farmer=farmer
    )

    return render(
        request,
        "marketplace/my_products.html",
        {
            "products": products
        }
    )


# ---------------- CUSTOMER PRODUCTS ----------------

def customer_products(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    products = Product.objects.all()

    search = request.GET.get("search")

    if search:
        products = products.filter(
            product_name__icontains=search
        )

    return render(
        request,
        "marketplace/customer_products.html",
        {
            "products": products,
            "search": search
        }
    )


# ---------------- BUY PRODUCT ----------------

def buy_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    customers = Customer.objects.all()

    if request.method == "POST":

        customer_id = request.POST.get("customer")
        quantity = int(request.POST.get("quantity"))

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        if quantity <= 0:
            return render(
                request,
                "marketplace/buy_product.html",
                {
                    "product": product,
                    "customers": customers,
                    "error": "Quantity must be greater than 0."
                }
            )

        if quantity > product.quantity:
            return render(
                request,
                "marketplace/buy_product.html",
                {
                    "product": product,
                    "customers": customers,
                    "error": "Not enough quantity available."
                }
            )

        total_price = product.price * quantity

        Order.objects.create(
            customer=customer,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        product.quantity -= quantity
        product.save()

        return redirect("customer_orders")

    return render(
        request,
        "marketplace/buy_product.html",
        {
            "product": product,
            "customers": customers
        }
    )


# ---------------- CUSTOMER ORDERS ----------------

def customer_orders(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    orders = Order.objects.filter(
        customer=customer
    ).order_by("-id")

    return render(
        request,
        "marketplace/customer_orders.html",
        {
            "orders": orders
        }
    )


# ---------------- FARMER ORDERS ----------------

def farmer_orders(request):

    farmer_id = request.session.get("farmer_id")

    if not farmer_id:
        return redirect("login")

    farmer = get_object_or_404(
        Farmer,
        id=farmer_id
    )

    orders = Order.objects.filter(
        product__farmer=farmer
    ).order_by("-id")

    return render(
        request,
        "marketplace/farmer_orders.html",
        {
            "orders": orders
        }
    )


# ---------------- LOGOUT ----------------

def logout_page(request):

    request.session.flush()

    return redirect("login")