from django.shortcuts import render
from commerce_app import views, models, urls, currency, admin
from commerce_app.views import *
from commerce_app.models import * 

# Create your views here.
@login_required
def panel_home(request):
    orders = Order.objects.all()
    profile_count = Profile.objects.count()
    order_count = Order.objects.count()
    print(orders)
    context = {
        'profile_count': profile_count,
        'orders': orders,
        'order_count': order_count,

    }

    return render(request, 'panel_home.html', context)

@login_required
def panel_orders(request):
    orders = Order.objects.all()
    order_count = Order.objects.count()
    print(orders)
    context = {
        'orders': orders,
        'order_count': order_count,
    }

    return render(request, 'panel_orders.html', context)

@login_required
def panel_order_detail(request, order_id):
    order_detail = get_object_or_404(Order, id=order_id)
    my_profile = Profile.objects.filter(user=request.user)
    usd =  currency.last_usd_data
    total_price = 0
    for item in order_detail.order_item.all():
        total_price += item.product.price * item.quantity * usd
        kdv = total_price * 0.20
        kdv_price = total_price * 1.20
        total_price_rounded = round(total_price, 4)
        kdv_rounded = round(kdv, 4)
        kdv_price_rounded = round(kdv_price, 4)

    
    context = {
        "total_price_rounded": total_price_rounded,
        "kdv_rounded": kdv_rounded,
        "kdv_price_rounded": kdv_price_rounded,
        'my_profile': my_profile,
        'order_detail': order_detail,
        'total_price': total_price,
        "kdv_price": kdv_price,
        "kdv":kdv,
    }
    return render(request, "panel_order_detail.html", context)

def panel_login(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("panel-home")
        else:
            return render(request, 'panel_login.html', {
                "error": "Kullanıcı adı veya parola yanlış."
            })

    return render(request, "panel_login.html")

def panel_logout(request):
    logout(request)
    return redirect("panel-login")
