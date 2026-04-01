from django.contrib import admin
from supplements.models import Supplements, Brand, Flavor, Product_content_size, Size, ImageSupplement, HomeBanner, Category, Feedback, FeedbackImage, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class FeedbackImageInline(admin.TabularInline):

    model = FeedbackImage
    extra = 0

@admin.action(description="Aprovar feedback selecionado")
def aprovar_feedback(modeladmin, request, queryset):
    queryset.update(is_approved=True)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "rating",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
    )

    search_fields = (
        "name",
        "comment",
    )

    list_editable = (
        "is_approved",
    )

    actions = [
        aprovar_feedback
    ]

    inlines = [
        FeedbackImageInline
    ]


admin.site.register(FeedbackImage)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image",)
    search_fields = ("name", "image",)
    ordering = ("name",)
 
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ("order", "is_active", "created_at", "link", "headline",)
    list_editable = ("is_active",)
    ordering = ("order",)

class ImageSupplementInline(admin.TabularInline):
    model = ImageSupplement
    extra = 4
    max_num = 4

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class Product_sizeAdmin(admin.ModelAdmin):
    list_display = ('display_size',)
    search_fields = ('value', 'unit')

    def display_size(self, obj):
        return str(obj)

    display_size.short_description = "Tamanho"   

class FlavordAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class SupplementAdmin(admin.ModelAdmin):
    list_display = ('model', 'get_first_price',)
    search_fields = ('model', 'variants__brand__name',)
    inlines = [ImageSupplementInline]
    inlines = [ProductVariantInline]

    def get_first_price(self, obj):
        variant = obj.variants.first()
        return variant.price if variant else "Sem variante"

    get_first_price.short_description = "Preço inicial"



admin.site.register(ProductVariant)   
admin.site.register(Category, CategoryAdmin)
admin.site.register(HomeBanner, HomeBannerAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Product_content_size, Product_sizeAdmin)
admin.site.register(Flavor, FlavordAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Supplements, SupplementAdmin)    
