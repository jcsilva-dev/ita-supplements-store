from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.utils import NotSupportedError
from decimal import Decimal
import uuid

class ProductVariant(models.Model):
    product = models.ForeignKey(
        'Supplements',
        on_delete=models.CASCADE,
        related_name='variants'
    )

    brand = models.ForeignKey(
        'Brand',
        on_delete=models.PROTECT,
        related_name='variants',
        verbose_name="Marca"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Preço"
    )

    size = models.ForeignKey(
        'Size',
        on_delete=models.PROTECT,
        related_name='variants',
        blank=True,
        null=True,
        verbose_name="Tamanho"
    )

    flavor = models.ForeignKey(
        'Flavor',
        on_delete=models.SET_NULL,
        related_name='variants',
        blank=True,
        null=True,
        verbose_name="Sabor"
    )

    product_content_size = models.ForeignKey(
        'Product_content_size',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='variants',
        verbose_name="Conteúdo"
    )

    # 🔥 NEVER NULL
    quantity_stock = models.PositiveIntegerField(default=0)

    sku = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.product.model} - {self.sku}"

    
    def is_available(self):
        return self.quantity_stock > 0

    
    def get_installment_options(
        self,
        max_installments=12,
        min_value=None,
        interest_rate=0
    ):
        options = []

        price = Decimal(str(self.price))
        interest_rate = Decimal(str(interest_rate))

        total_price = price

        if interest_rate > 0:
            total_price = price * (Decimal("1") + interest_rate)

        for i in range(1, max_installments + 1):

            installment_value = (total_price / Decimal(i)).quantize(Decimal("0.01"))

            if min_value and installment_value < Decimal(str(min_value)):
                continue

            options.append({
                "times": i,
                "value": installment_value
            })

        return options  

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Order {self.code}"
    

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,   
        blank=True,
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    installments = models.IntegerField(null=True, blank=True)

    def subtotal(self):
        return self.quantity * self.unit_price



class Feedback(models.Model):

    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.rating} estrelas"
    
class FeedbackImage(models.Model):

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to="feedbacks/"
    )
    def __str__(self):
        return f"Imagem de {self.feedback.name}"
    

class SupplementQuerySet(models.QuerySet):

    def get_recommended(self, product):
        same_category = (
            self.filter(category=product.category)
            .exclude(id=product.id)
            .order_by('-total_visualizacoes')[:4]
        )

        if len(same_category) >= 4:
            return same_category 

        return (
            self.exclude(id=product.id)
            .order_by('-total_visualizacoes')[:4]
        )


class SupplementManager(models.Manager):

    def get_queryset(self):
        return SupplementQuerySet(self.model, using=self._db)

    def get_recommended(self, product):
        return self.get_queryset().get_recommended(product)
    

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/default-category.png"

    


class Size(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product_content_size(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=20)
  
    def __str__(self):
        return f"{self.value} {self.unit}"

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Flavor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Supplements(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=200, verbose_name="Modelo")

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='supplements',
        null=True,
        blank=True,
        verbose_name="Categoria"
    )

    description = models.TextField(blank=True, null=True)
    total_visualizacoes = models.PositiveIntegerField(default=0)

    objects = SupplementManager()

    def get_main_image(self):
      image = self.images.first()
      return image.photo.url if image and image.photo else None

    def __str__(self):
        return self.model

    # 🔥 QUERY OTIMIZADA
    def get_variants(self):
        return self.variants.select_related(
            'brand',
            'size',
            'flavor',
            'product_content_size'
        )

    # 🔥 REGRA DE NEGÓCIO: variante padrão
    def get_default_variant(self):
        variants = self.get_variants()

        variant = variants.filter(quantity_stock__gt=0).order_by('price').first()

        return variant or variants.order_by('price').first()

    # 🔥 ATRIBUTOS PARA UI
    def get_available_attributes(self):
        variants = self.get_variants()

        return {
            "sizes": list(
                variants.exclude(size__isnull=True)
                .values_list('size__name', flat=True)
                .distinct()
            ),
            "flavors": list(
                variants.exclude(flavor__isnull=True)
                .values_list('flavor__name', flat=True)
                .distinct()
            ),
        }

    # 🔥 PREÇO BASE (usado em listagem)
    def get_price(self):
        variant = self.variants.only('price').order_by('price').first()
        return variant.price if variant else 0

    # 🔥 MAPA PARA FRONTEND (CRÍTICO)
    def get_variant_map(self):
        variants = self.get_variants()

        data = {}

        for v in variants:
            key = f"{v.flavor_id}_{v.size_id}"

            data[key] = {
                "id": v.id,
                "price": float(v.price),
                "stock": v.quantity_stock,
            }

        return data

    
class ImageSupplement(models.Model):
    supplement = models.ForeignKey(Supplements, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='Supplements/')
    
    MAX_IMAGES = 4 

    def save(self, *args, **kwargs):
        if not self.supplement_id:
            raise ValidationError("Você precisa escolher um produto.")

        with transaction.atomic():

            try:
                supplement_model = self._meta.get_field("supplement").remote_field.model
                supplement_model.objects.select_for_update().get(pk=self.supplement_id)
            except NotSupportedError:
                pass

        
            total_images = ImageSupplement.objects.filter(
                supplement_id=self.supplement_id
            ).exclude(pk=self.pk).count()

            if total_images >= self.MAX_IMAGES:
                raise ValidationError(
                    f"Este produto já possui o máximo de {self.MAX_IMAGES} imagens."
                )

            super().save(*args, **kwargs)

    def __str__(self):
        return f"Imagem do produto: {self.supplement}" 
    


class HomeBanner(models.Model):
    image = models.ImageField(upload_to="home_banners/", help_text="imagen do banner. sugestao: 1920x500 ou 1600x450")
    headline = models.CharField(max_length=100, blank=True, help_text="Texto opcional do banner (se quiser mostrar em cima).")
    link = models.URLField(blank=True, help_text="Link opcional. Se preencher, ao clicar no banner vai abrir esse link.")
    order = models.PositiveBigIntegerField(default=1, help_text="Ordem de exibição (1, 2, 3).")
    is_active = models.BooleanField(default=True, help_text="Se desativar, esse banner não aparece no site.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"Banner {self.order}"
    

    
