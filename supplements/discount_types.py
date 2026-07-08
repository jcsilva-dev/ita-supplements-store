from decimal import Decimal
from dataclasses import dataclass


@dataclass(frozen=True)
class DiscountResult:
    """
    Representa o resultado de um cálculo de desconto.
    """

    original_price: Decimal
    discount_price: Decimal
    discount_value: Decimal
    percentage: Decimal
    has_discount: bool
    @property

    def economy(self):

        return self.discount_value