def categories_global(request):
    from .models import Category  

    return {
        "categories": Category.objects.all()
    }


def cart_count(request):
    cart = request.session.get("cart", {})

    total_items = sum(
        item["quantity"]
        for item in cart.values()
    )

    return {
        "cart_count": total_items
    }