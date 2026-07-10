from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from supplements.models import Supplements, HomeBanner, Category, Feedback, FeedbackImage
from supplements.forms import SupplementModelForm, ImageFormSet, FeedbackForm, VariantFormSet
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect 
from supplements.services import DiscountService


class CategorySupplementView(ListView):
    model = Supplements
    template_name = "category.html"
    context_object_name = "supplements"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category")

        slug = self.kwargs.get("slug")

        if slug and slug != "all":
            queryset = queryset.filter(category__slug=slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get("slug")

        if slug == "all":
            context["category"] = None
        else:
            context["category"] = Category.objects.filter(slug=slug).first()

        return context

class SupplementsView(ListView):
     model = Supplements
     template_name = 'suplementos.html'
     context_object_name = 'supplements'

class SupplementsView(ListView):
     model = Supplements
     template_name = "suplementos.html"
     context_object_name = "supplements"

     def get_queryset(self):
        search = self.request.GET.get("search")

        return (
            Supplements.objects
            .order_by("model")
            .search(search)
        )
     
     def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["banners"] = HomeBanner.objects.filter(is_active=True).order_by("order")[:5]
      context["campaign_banner"] = DiscountService.get_banner()

      for supplement in context["supplements"]:

          variant = supplement.get_default_variant()

          if variant:
              supplement.discount = (
                  DiscountService.get_product_price(variant)
              )
          else:
               supplement.discount = None

      return context
       
@method_decorator(login_required(login_url='login'), name='dispatch')
class NewSuplementView(CreateView):
    model = Supplements
    form_class = SupplementModelForm
    template_name = 'new_supplement.html'
    success_url = '/supplements/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "formset" in kwargs:
            context["formset"] = kwargs["formset"]
        else:
            context["formset"] = ImageFormSet()

        if "variant_formset" in kwargs:
            context["variant_formset"] = kwargs["variant_formset"]
        else:
            context["variant_formset"] = VariantFormSet()

        return context

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()

        formset = ImageFormSet(
            self.request.POST,
            self.request.FILES
        )

        variant_formset = VariantFormSet(
            self.request.POST
        )

        if (
            form.is_valid()
            and formset.is_valid()
            and variant_formset.is_valid()
        ):
            return self.forms_valid(
                form,
                formset,
                variant_formset
            )

        return self.forms_invalid(
            form,
            formset,
            variant_formset
        )

    def forms_valid(
        self,
        form,
        formset,
        variant_formset
    ):
        with transaction.atomic():

            self.object = form.save()

            formset.instance = self.object
            formset.save()

            variant_formset.instance = self.object
            variant_formset.save()

        return super().form_valid(form)

    def forms_invalid(
        self,
        form,
        formset,
        variant_formset
    ):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset,
                variant_formset=variant_formset
            )
        )


class SupplementDetailView(DetailView):
    model = Supplements
    template_name = 'supplement_detail.html'
    context_object_name = 'supplement'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        Supplements.objects.filter(pk=obj.pk).update(
            total_visualizacoes=F('total_visualizacoes') + 1
        )

        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object  

        variants = product.get_variants()

        default_variant = product.get_default_variant()

        default_price_info = DiscountService.get_product_price(default_variant)

        attributes = product.get_available_attributes()

        installments = default_variant.get_installment_options(price=default_price_info.discount_price)

        
        for variant in variants:

            variant.price_info = DiscountService.get_product_price(variant)

            variant.installments = variant.get_installment_options(
                price=variant.price_info.discount_price
            )
            print(
                "VARIANTE:", variant.id,
                "| PREÇO:", variant.price_info.discount_price,
                "| PRIMEIRA PARCELA:",
                variant.installments[0]["value"] if variant.installments else "SEM PARCELAS"
            )

        context.update({
            "variants": variants,
            "default_variant": default_variant,
            "price_info": default_price_info,
            "sizes": attributes["sizes"],
            "flavors": attributes["flavors"],
            "installments": installments if default_variant else [],
      })

        
        context["recommended_products"] = Supplements.objects.get_recommended(product)

        context["feedbacks"] = Feedback.objects.filter(is_approved=True)

        context["feedback_form"] = FeedbackForm()

        return context

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)

        if form.is_valid():
            feedback = form.save()

            images = request.FILES.getlist("images")

            for img in images:
                FeedbackImage.objects.create(
                    feedback=feedback,
                    image=img
                )

        return redirect(request.path)
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class SupplementUpdateView(UpdateView):
    model = Supplements
    form_class = SupplementModelForm
    template_name = 'supplement_update.html'

    def get_success_url(self):
        return reverse_lazy('supplement_detail', kwargs={'pk':self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["formset"] = ImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )

            context["variant_formset"] = VariantFormSet(
                self.request.POST,
                instance=self.object
)
        else:
            context["formset"] = ImageFormSet(instance=self.object)
            context["variant_formset"] = VariantFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        variant_formset = context["variant_formset"]

        if (
            not formset.is_valid()
            or not variant_formset.is_valid()
        ):
            return self.form_invalid(form)
        
        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            variant_formset.instance = self.object
            variant_formset.save()
            formset.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class SupplementDeleteView(DeleteView):
    model = Supplements
    template_name = 'supplement_delete.html'
    success_url = '/supplements/'

