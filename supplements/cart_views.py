from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Supplements, Order, OrderItem
from .utils import build_whatsapp_message
import urllib.parse


def add_to_cart(request, product_id):

    if request.method != "POST":
        return redirect("supplements")

    product = get_object_or_404(Supplements, id=product_id)

    action = request.POST.get("action")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    try:
        installments = int(request.POST.get("installments", 1))
    except ValueError:
        installments = 1

    product_key = str(product_id)

    print("ACTION:", action)

    
    if action == "buy":

        subtotal = product.price * quantity

        message = "🛒 *Novo Pedido*\n\n"

        message = build_whatsapp_message(product, quantity)


        if installments > 1:

            installment_value = round(subtotal / installments, 2)

            message += (
                f"💳 Parcelamento: {installments}x de R$ {installment_value:.2f}\n"
            )

        message += "\nGostaria de finalizar esse pedido."

        message = urllib.parse.quote(message, safe="")

        return redirect(
            f"https://wa.me/5583991771531?text={message}"
        )

    
    elif action == "cart":

        cart = request.session.get("cart", {})

        if product_key in cart:

            cart[product_key]["quantity"] += quantity
            cart[product_key]["installments"] = installments

        else:

            cart[product_key] = {
                "quantity": quantity,
                "installments": installments
            }

        request.session["cart"] = cart

        return redirect("cart")

    return redirect("cart")


def cart_view(request):

    cart = request.session.get("cart", {})

    products = []

    total = Decimal("0.00")

    for product_id, item in cart.items():

        product = get_object_or_404(Supplements, id=product_id)
        quantity = item["quantity"]

        subtotal = product.price * quantity

        installments = item.get("installments", 1)

        installment_value = subtotal / installments

        products.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
            "installments": installments,
            "installment_value": installment_value
        })

        total += subtotal

    context = {
        "products": products,
        "total": total
    }

    return render(request, "carrinho.html", context)


def remove_item(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


def finalize_order(request):

    cart = request.session.get("cart", {})

    print("CARRINHO:", cart)

    if not cart:
        return redirect("cart")

    order = Order.objects.create(status="pending")

    total = Decimal("0.00")

    
    cart_installments = request.POST.get("cart_installments")

    message = f"🛒 *Novo Pedido #{order.code}*\n\n"

    for product_id, item in cart.items():

        product = get_object_or_404(Supplements, id=product_id)

        quantity = item["quantity"]

        installments = item.get("installments", 1)

        subtotal = product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.price,
            installments=installments if not cart_installments else cart_installments
        )

        message += build_whatsapp_message(product, quantity)

       
        if not cart_installments:

           installments = item.get("installments")
        
           if installments and installments >1:
                installment_value = subtotal / installments

                message += (
                  f"💳 Parcelamento: {installments}x de R$ {installment_value:.2f}\n"
                )

        message += "\n"

        total += subtotal

    order.total = total
    order.save()

    
    if cart_installments:

        cart_installments = int(cart_installments)

        installment_value = total / cart_installments

        message += (
            f"💳 *Parcelamento do Pedido:* {cart_installments}x de R$ {installment_value:.2f}\n\n"
        )

    message += f"🚚 Frete: Grátis\n"
    message += f"💵 *Total do Pedido: R$ {total}*\n\n"
    message += "Gostaria de finalizar esse pedido."

    message = urllib.parse.quote(message, safe="")

    request.session["cart"] = {}

    return redirect(
        f"https://wa.me/5583991771531?text={message}"
    )