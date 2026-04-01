from decimal import Decimal, ROUND_HALF_UP
from django.urls import reverse

def build_whatsapp_message(items, installments=None, request=None):

    if not isinstance(items, list):
        items = [items]

    total = Decimal("0.00")

    message = "👋 Olá! Tudo bem?\n\n"
    message += "Acabei de fazer um pedido pelo site.\n\n"
    message += "━━━━━━━━━━━━━━━━━━\n\n"

    for item in items:

        variant = item["variant"]
        quantity = item["quantity"]

        price = variant.price
        subtotal = price * quantity
        total += subtotal

        product_url = ""
        if request:
            product_url = request.build_absolute_uri(
                reverse("supplement_detail", args=[variant.product.id])
            )

        message += f"📦 *Produto:* {variant.product.model}\n"

        if getattr(variant, "brand", None):
            message += f"🏷 Marca: {variant.brand}\n"

        if getattr(variant, "flavor", None):
            message += f"🍫 Sabor: {variant.flavor}\n"

        if getattr(variant, "size", None):
            message += f"📏 Tamanho: {variant.size}\n"

        message += f"🔢 Quantidade: {quantity}\n"
        message += f"💰 Subtotal: R$ {subtotal:.2f}\n"

       
        if product_url:
           message += f"🔗 {product_url}\n" 

        message += "\n━━━━━━━━━━━━━━━━━━\n\n"

    if installments and installments > 1:
        installment_value = (total / installments).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        message += f"💳 Parcelamento: {installments}x de R$ {installment_value}\n\n"

    message += f"💰 *Total:* R$ {total:.2f}\n\n"
    message += "Gostaria de finalizar esse pedido 😊"

    return message