def categories_global(request):
    from .models import Category  

    return {
        "categories": Category.objects.all()
    }