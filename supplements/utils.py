
def build_whatsapp_message(product, quantity):

    
    subtotal = product.price * quantity

    
    product_url = f"https://seudominio.com/supplements/{product.id}/"

    message = (
        "👋 Olá! Tudo bem?\n\n"
        "Acabei de fazer um pedido pelo site e gostaria de finalizar a compra.\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 Produto: {product.model}\n"
    )

  
    if getattr(product, "brand", None):
        message += f"🏷 Marca: {product.brand}\n"

    
    if getattr(product, "category", None):
        message += f"📂 Categoria: {product.category.name}\n"

   
    if getattr(product, "flavor", None):
        message += f"🍫 Sabor: {product.flavor}\n"

    
    if getattr(product, "size", None):
        message += f"📏 Tamanho: {product.size}\n"

    
    if getattr(product, "product_content_size", None):
        message += f"⚖ Conteúdo: {product.product_content_size}\n"

    message += f"\n🔗 Ver produto: {product_url}\n"

    
    message += (
        f"\n🔢 Quantidade: {quantity}\n"
        f"💰 Preço unitário: R$ {product.price}\n"
        f"📊 Total: R$ {subtotal}\n"
    )

    return message

