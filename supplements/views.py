from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from supplements.models import Supplements, HomeBanner, Category, Feedback, FeedbackImage
from supplements.forms import SupplementModelForm, ImageFormSet, FeedbackForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect 



class CategorySupplementView(ListView):
    model = Supplements
    template_name = "category.html"
    context_object_name = "supplements"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("category")
        category_id = self.request.GET.get("category")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class SupplementsView(ListView):
     model = Supplements
     template_name = 'suplementos.html'
     context_object_name = 'supplements'

     def get_queryset(self):
       supplements = super().get_queryset().order_by('model')
       search = self.request.GET.get('search')

       if search:
           supplements = supplements.filter(model__icontains=search)

       return supplements
     
     def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)

      context["banners"] = HomeBanner.objects.filter(is_active=True).order_by("order")[:5]

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

        return context

  
     def post(self, request, *args, **kwargs):
        self.object = None  

        form = self.get_form()
        formset = ImageFormSet(self.request.POST, self.request.FILES)

        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)

        return self.forms_invalid(form, formset)

     def forms_valid(self, form, formset):
        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

     def forms_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )
     
     


class SupplementDetailView(DetailView):
    model = Supplements
    template_name = 'supplement_detail.html'
    context_object_name = 'supplement'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

       
        obj.total_visualizacoes = F('total_visualizacoes') + 1
        obj.save(update_fields=['total_visualizacoes'])
        obj.refresh_from_db()

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        produto = self.object

        context["recomendacoes"] = (
            Supplements.objects
            .recomendados(produto)[:4]
        )

       
        context["feedbacks"] = Feedback.objects.filter(
            is_approved=True
        )

        
        context["feedback_form"] = FeedbackForm()
         
        
        context["installments"] = produto.get_installment_options()

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
        else:
            context["formset"] = ImageFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        if not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
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

