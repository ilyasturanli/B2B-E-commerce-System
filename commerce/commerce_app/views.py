from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
import pywhatkit as kit
import datetime
import threading
from . import currency


# WhatsApp mesajını arka planda gönderecek fonksiyon
def send_whatsapp_message(username):
    try:
        kit.sendwhatmsg_instantly(
            "+905350244973",  # kendi numaran
            f"{username} adlı kullanıcı yeni bir sipariş verdi.",
            wait_time=10,
            tab_close=True
        )
    except Exception as e:
        print("WhatsApp mesajı gönderilemedi:", e)


@login_required
def home(request):
    currency_usd = currency.last_usd_data
    cart_products = Cart.objects.filter(user=request.user)
    cart_count = cart_products.count()
    products = Product.objects.all()
    brands = Brand.objects.all()
    sub_models = SubModel.objects.all()
    sizes = Size.objects.all()
    sliders = Slider.objects.all()

    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(content__icontains=query)
        )

    if "submodel" in request.GET and request.GET.get("submodel") != "":
        submodel_id = request.GET.get("submodel")
        submodel = SubModel.objects.get(id=submodel_id)
        products = Product.objects.filter(brand=submodel)

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        size_id = request.POST.get("size_id", 1)
        size = Size.objects.get(id=size_id)
        product = Product.objects.get(id=product_id)

        cart_product = Cart.objects.filter(user=request.user, product=product, feature=size).first()
        if cart_product:
            cart_product.quantity += 1
            cart_product.save()
            messages.success(request, f"{product.name} adlı ürünün miktarı güncellendi.")
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1, feature=size)
            messages.success(request, "Ürün sepetinize eklendi.")

    context = {
        'sizes': sizes,
        'sub_models': sub_models,
        'cart_count': cart_count,
        "cart_products": cart_products,
        'products': products,
        'brands': brands,
        'sliders': sliders,
        "currency_usd": currency_usd
    }
    return render(request, "home.html", context)


@login_required
def detail(request, product_id):
    currency_usd = currency.last_usd_data
    cart_count = Cart.objects.filter(user=request.user).count()
    product_detail = get_object_or_404(Product, id=product_id)
    products = Product.objects.all()

    context = {
        'cart_count': cart_count,
        'product_detail': product_detail,
        'products': products,
        "currency_usd": currency_usd
    }
    return render(request, "detail.html", context)


@login_required
def cart(request):
    currency_usd = currency.last_usd_data
    cart_products = Cart.objects.filter(user=request.user).order_by("id")
    cargos = Cargo.objects.all()
    cart_count = cart_products.count()
    usd = currency_usd

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if request.POST.get("submit") == "btndel":#Soldaki hmtldeki name = , sagdaki htmldeki value = degerdir...
            Cart.objects.get(id=product_id).delete()
            return redirect("cart")

        elif request.POST.get("submit") == "minus":
            product = Cart.objects.get(id=product_id)
            if product.quantity > 1:
                product.quantity -= 1
                product.save()
            else:
                product.delete()
            return redirect("cart")

        elif request.POST.get("submit") == "plus":
            product = Cart.objects.get(id=product_id)
            product.quantity += 1
            product.save()
            return redirect("cart")

        elif request.POST.get("order-submit") == "ordersubmit":
            cargo_id = request.POST.get("cargo")#htmldeki name = cargo dan geliyor...
            cargo = Cargo.objects.get(id=cargo_id)
            products = Cart.objects.filter(user=request.user)
            order_items = []

            for product in products:
                order_item = OrderItem.objects.create(
                    product=product.product,
                    quantity=product.quantity,
                    size=product.feature,
                )
                order_items.append(order_item)

            new_order = Order.objects.create(user=request.user, cargo=cargo)
            for item in order_items:
                new_order.order_item.add(item)
            new_order.save()
            products.delete()

            # WhatsApp mesajını arka planda gönder
            threading.Thread(target=send_whatsapp_message, args=(request.user.username,)).start()

            return redirect("order-success")

    total_price = sum([p.product.price * p.quantity * usd for p in cart_products])
    kdv = total_price * 0.20
    kdv_price = total_price * 1.20

    context = {
        'cargos': cargos,
        'cart_count': cart_count,
        "cart_products": cart_products,
        "total_price": total_price,
        "kdv_price": kdv_price,
        "kdv": kdv,
        "usd_product": 0,
        "total_price_rounded": round(total_price, 4),
        "kdv_rounded": round(kdv, 4),
        "kdv_price_rounded": round(kdv_price, 4),
        "currency_usd": currency_usd,
    }
    return render(request, "cart.html", context)


@login_required
def order_success(request):
    currency_usd = currency.last_usd_data
    sub_models = SubModel.objects.all()
    sizes = Size.objects.all()
    return render(request, "order_success.html", {
        "currency_usd": currency_usd,
        'sizes': sizes,
        'sub_models': sub_models,
    })


@login_required
def order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order.html", {"orders": orders})


@login_required
def profile(request):
    currency_usd = currency.last_usd_data
    cart_count = Cart.objects.filter(user=request.user).count()
    orders = Order.objects.filter(user=request.user)
    my_profile = Profile.objects.filter(user=request.user)
    profiles = User.objects.filter(username=request.user.username)
    return render(request, "profile.html", {
        'my_profile': my_profile,
        'orders': orders,
        'cart_count': cart_count,
        'profiles': profiles,
        'currency_usd': currency_usd,
    })


@login_required
def order_detail(request, order_id):
    order_detail = get_object_or_404(Order, id=order_id)
    currency_usd = currency.last_usd_data
    usd = currency_usd
    my_profile = Profile.objects.filter(user=request.user)

    total_price = sum([item.product.price * item.quantity * usd for item in order_detail.order_item.all()])
    kdv = total_price * 0.20
    kdv_price = total_price * 1.20

    context = {
        "total_price_rounded": round(total_price, 4),
        "kdv_rounded": round(kdv, 4),
        "kdv_price_rounded": round(kdv_price, 4),
        'my_profile': my_profile,
        'order_detail': order_detail,
        'total_price': total_price,
        "kdv_price": kdv_price,
        "kdv": kdv,
        'currency_usd': currency_usd,
    }
    return render(request, "order_detail.html", context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Kullanıcı adı veya parola yanlış."})
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("user-login")
