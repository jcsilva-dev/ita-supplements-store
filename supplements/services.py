from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from .discount_types import DiscountResult
from .models import Campaign


HUNDRED = Decimal("100")


class DiscountService:

    @staticmethod
    def get_active_campaign():
        """
        Retorna a campanha global ativa.

        Caso não exista nenhuma campanha válida,
        retorna None.
        """

        now = timezone.now()

        return (
            Campaign.objects
            .filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now,
            )
            .first()
        )

    @staticmethod
    def has_active_campaign():
        """
        Verifica se existe uma campanha ativa.

        Returns:
        bool: true caso exista uma campanha ativa.
        """
        return DiscountService.get_active_campaign() is not None  

    @staticmethod
    def calculate_discount(price):
        """
        Calcula o desconto de um preço utilizando
        a campanha ativa.

        Args:
            price (Decimal): preço original

        Returns:
            DiscountResult: resultado do cálculo do desconto.
        """


        campaign = DiscountService.get_active_campaign()

        price = Decimal(str(price))
        
        
        
        if not campaign:
            return DiscountResult(
                original_price=price,
                discount_price=price,
                discount_value=Decimal("0.00"),
                percentage=Decimal("0.00"),
                has_discount=False,
            )

        percentage = campaign.discount_percentage

        discount_value = (
            price * percentage / HUNDRED
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        final_price = (
            price - discount_value
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        return DiscountResult(
            original_price=price,
            discount_price=final_price,
            discount_value=discount_value,
            percentage=percentage,
            has_discount=True,
        )
    

    @staticmethod
    def get_product_price(variant):
        """
        Retorna todas as informações de preço de uma variante.

        Esse método deve ser utilizado por qualquer View,
        Template ou lógica que precise mostrar o preço
        de um produto.

        Args:
            variant (ProductVariant)

        Returns:
            DiscountResult
        """
        if variant is None:
            return None

        return DiscountService.calculate_discount(
            variant.price
        )

    @staticmethod
    def get_banner():
        """
        Retorna a campanha ativa para exibição no banner
        da loja.

        Returns:
            Campaign | None
        """

        return DiscountService.get_active_campaign()

