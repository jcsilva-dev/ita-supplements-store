from supplements.models import Supplements, ImageSupplement, Feedback, ProductVariant
from django import forms 
from django.forms import inlineformset_factory


class SupplementModelForm(forms.ModelForm):
    class Meta:
     model = Supplements
     fields = '__all__'



VariantFormSet = inlineformset_factory(
    Supplements,
    ProductVariant,
    fields=[
        "price",
        "size",
        "flavor",
        "product_content_size",
        "quantity_stock",
    ],
    extra=3,
    can_delete=True
)

ImageFormSet = inlineformset_factory(
   Supplements,
   ImageSupplement,
   fields=('photo',),
   extra=4,
   max_num=4,
   can_delete=True
)




class FeedbackForm(forms.ModelForm):

    class Meta:

        model = Feedback

        fields = ["name", "rating", "comment" ]

        labels = {
            "name": "Seu nome",
            "rating": "Avaliação do produto",
            "comment": "Seu comentário",
        }

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Escreva seu nome",
                    "class": "input-feedback"
                }
            ),

            "rating": forms.Select(
                attrs={
                    "class": "select-feedback"
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "placeholder": "Conte como foi sua experiência com o produto",
                    "rows": 4,
                    "class": "textarea-feedback"
                }
            ),
        }
