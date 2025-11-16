from .models import Product, StockVariant
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .forms import ProductForm, StockVariantInlineFormset
from django.http import JsonResponse


# Create your views here.

class ProductListView(ListView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product/product_create.html'
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        # Create the Product form
        form = self.get_form()
        # Create an empty formset for StockVariant
        formset = StockVariantInlineFormset(queryset=StockVariant.objects.none())
        return self.render_to_response({'form': form, 'formset': formset, 'business_id': self.kwargs.get('business_id')})

    def post(self, request, *args, **kwargs):
        # Create the Product form
        form = self.get_form()
        # Create the StockVariant formset
        formset = StockVariantInlineFormset(request.POST)

        if form.is_valid() and formset.is_valid():
            # Save the Product (one Product)
            product = form.save()

            # Save the StockVariants and associate each with the created Product
            stock_variants = formset.save(commit=False)
            for stock_variant in stock_variants:
                stock_variant.product = product  # Associate StockVariant with the Product
                stock_variant.save()

            return redirect('product-list')

        return self.render_to_response({'form': form, 'formset': formset})



def product_search_ajax_view(request):
    """
    Handles Select2 AJAX search requests for product items tied to a specific business.
    """
    # 1. Get the search term from the AJAX request (Select2 passes it as 'term')
    search_term = request.GET.get('term', '')

    # 2. Query the database
    # CRITICAL: Filter by business_id first for security and context
    products_queryset = Product.objects.all()

    # Filter based on the search term (case-insensitive contains lookup)
    if search_term:
        products_queryset = products_queryset.filter(
            name__icontains=search_term
        )
    
    # Limit the results for performance (Select2 usually fetches 10-30 items per request)
    products = products_queryset[:30] 

    # 3. Format the data for Select2
    # Select2 requires a list of dictionaries with 'id' and 'text' keys
    results = []
    for product in products:
        results.append({
            'id': product.pk,          # The value to be stored in the model field
            'text': product.name       # The text displayed to the user
        })

    # 4. Return the response
    return JsonResponse({
        'results': results,
        # 'pagination' key is needed if you implement scrolling/loading more results
        'pagination': {
            'more': products_queryset.count() > len(products) 
        }
    })








