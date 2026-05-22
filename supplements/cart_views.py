from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import ProductVariant
from .utils import build_whatsapp_message
import urllib.parse
from django.contrib import messages




def add_to_cart(request):


   if request.method != "POST":
       return redirect("supplements")


   variant_id = request.POST.get("variant_id")


   if not variant_id:
       messages.error(request, "Variante não enviada")
       return redirect("supplements")


  
   variant = get_object_or_404(
       ProductVariant.objects.select_related(
           "product",
           "size",
           "flavor"
       ),
       id=variant_id
   )


  
   if not variant.is_available():
       messages.error(request, "Produto esgotado")
       return redirect(request.META.get("HTTP_REFERER", "supplements"))


   action = request.POST.get("action")


   quantity = int(request.POST.get("quantity", 1) or 1)
   quantity = max(quantity, 1)


   installments = int(request.POST.get("installments", 1) or 1)
   installments = max(installments, 1)


   if action == "buy":


       items = [{"variant": variant, "quantity": quantity}]


       message = build_whatsapp_message(
           items=items,
           installments=installments,
           request=request
       )


       return redirect(
           f"https://wa.me/5583991771531?text={urllib.parse.quote_plus(message)}"
       )


   if action == "cart":


       cart = request.session.get("cart", {})
       key = str(variant.id)


       if key in cart:
           cart[key]["quantity"] += quantity
       else:
           cart[key] = {
               "variant_id": variant.id,
               "product_id": variant.product.id,
               "product_name": variant.product.model,
               "sku": variant.sku,
               "price": float(variant.price),
               "quantity": quantity,
               "size": variant.size.name if variant.size else "",
               "flavor": variant.flavor.name if variant.flavor else "",
           }


       request.session["cart"] = cart
       request.session.modified = True


       messages.success(request, "Produto adicionado ao carrinho")


       return redirect("cart")


   return redirect("supplements")




def cart_view(request):


   cart = request.session.get("cart", {})
   items = []
   total = Decimal("0.00")


   if not cart:
       return render(request, "carrinho.html", {
           "items": [],
           "total": total
       })


   variant_ids = list(set(item["variant_id"] for item in cart.values()))


   variants = (
       ProductVariant.objects
       .select_related(
           "product",
           "size",
           "flavor",
           "product_content_size"
       )
       .prefetch_related("product__images") 
       .filter(id__in=variant_ids)
   )


   variant_map = {v.id: v for v in variants}


   for key, item in cart.items():


       variant = variant_map.get(item["variant_id"])


       if not variant:
           continue


       price = variant.price
       quantity = item["quantity"]
       subtotal = price * quantity


      
       image = variant.product.get_main_image()


       items.append({
           "key": key,
           "variant_id": variant.id,
           "product_id": variant.product.id,


           "product_name": variant.product.model,


           "sku": variant.sku,


           "size": variant.size.name if variant.size else "",
           "flavor": variant.flavor.name if variant.flavor else "",


           "quantity": quantity,


           "price": price,
           "subtotal": subtotal,


           "image": image,


           "stock": variant.quantity_stock,
       })


       total += subtotal


   return render(request, "carrinho.html", {
       "items": items,
       "total": total
   })




def remove_item(request, key):


   cart = request.session.get("cart", {})


   if str(key) in cart:
       del cart[key]
       request.session.modified = True
       messages.info(request, "Item removido")


   return redirect("cart")




def finalize_order(request):


   if request.method != "POST":
       return redirect("cart")


   cart = request.session.get("cart", {})


   if not cart:
       messages.warning(request, "Carrinho vazio")
       return redirect("cart")


   installments = int(request.POST.get("cart_installments") or 1)
   installments = max(installments, 1)


   items = []


   variants = (
   ProductVariant.objects
   .select_related(
       "product",
       "size",
       "flavor"
   )
   .filter(
       id__in=[item["variant_id"] for item in cart.values()]
   )
)


   variant_map = {v.id: v for v in variants}


   for item in cart.values():
       variant = variant_map.get(item["variant_id"])


       if not variant:
           continue
      
       if not variant.is_available():
           messages.error(
               request,
               f"{variant.product.model} está sem estoque."
           )
           return redirect("cart")
      
       if item["quantity"] > variant.quantity_stock:
           messages.error(
               request,
               f"Estoque insuficiente para {variant.product.model}."
           )
           return redirect("cart")
   
       items.append({
           "variant": variant,
           "quantity": item["quantity"]
       })


   if not items:
       return redirect("cart")
  
   message = build_whatsapp_message(
       items=items,
       installments=installments,
       request=request
   )
  
   request.session["cart"] = {}
   request.session.modified = True


   return redirect(
       f"https://wa.me/5583991771531?text={urllib.parse.quote_plus(message)}"
   )
