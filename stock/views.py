from .models import Stock
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.


class StockListView(LoginRequiredMixin, ListView):
    model = Stock


class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    fields = ['name', 'stock_type','opening_quantity']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Common classes for text/number inputs
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        
        # Classes for the select dropdown
        select_classes = 'form-select appearance-none flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 pl-4 pr-10 text-base font-normal leading-normal'

        form.fields['name'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., CR7'})
        form.fields['opening_quantity'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 100'})
        form.fields['stock_type'].widget.attrs.update({'class': select_classes})
        return form


class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = Stock
    fields = ['name', 'stock_type', 'opening_quantity']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Common classes for text/number inputs
        input_classes = 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 p-4 text-base font-normal leading-normal'
        
        # Classes for the select dropdown
        select_classes = 'form-select appearance-none flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-neutral-500 focus:outline-0 focus:ring-1 focus:ring-primary border border-slate-300 dark:border-neutral-700 bg-slate-100/50 dark:bg-neutral-900/50 h-14 pl-4 pr-10 text-base font-normal leading-normal'

        form.fields['name'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., CR7'})
        form.fields['opening_quantity'].widget.attrs.update({'class': input_classes, 'placeholder': 'e.g., 100'})
        form.fields['stock_type'].widget.attrs.update({'class': select_classes})
        return form

@login_required
def stock_search_ajax_view(request):
    """
    Handles Select2 AJAX search requests for Stock items tied to a specific business.
    """
    # 1. Get the search term from the AJAX request (Select2 passes it as 'term')
    search_term = request.GET.get('term', '')

    # 2. Query the database
    # CRITICAL: Filter by business_id first for security and context
    stocks_queryset = Stock.objects.all()

    # Filter based on the search term (case-insensitive contains lookup)
    if search_term:
        stocks_queryset = stocks_queryset.filter(
            name__icontains=search_term
        )
    
    # Limit the results for performance (Select2 usually fetches 10-30 items per request)
    stocks = stocks_queryset[:30] 

    # 3. Format the data for Select2
    # Select2 requires a list of dictionaries with 'id' and 'text' keys
    results = []
    for stock in stocks:
        results.append({
            'id': stock.pk,          # The value to be stored in the model field
            'text': stock.name       # The text displayed to the user
        })

    # 4. Return the response
    return JsonResponse({
        'results': results,
        # 'pagination' key is needed if you implement scrolling/loading more results
        'pagination': {
            'more': stocks_queryset.count() > len(stocks) 
        }
    })
