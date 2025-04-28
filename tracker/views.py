from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
from tracker.models import Transaction
from tracker.filters import TransactionFilter
from tracker.forms import TransactionForm
from django_htmx.http import retarget
from tracker.charting import plot_income_expenses_bar_chart, plot_category_pie_chart
from tracker.resources import TransactionResource
from django.http import HttpResponse
from tablib import Dataset
from sms.models import Lichhoc, LopMonhoc, Lop, Monhoc
from django.db.models import Q



# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(1) # default to 1 when this view is triggered

    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        'transactions': transaction_page,
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses
    }

    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)

    return render(request, 'tracker/transactions-list.html', context)

@login_required(login_url='/accounts/login/')
def lichhoc_list(request):
    lh = Lichhoc.objects.all()
    paginator = Paginator(lh, 20)
    transaction_page = paginator.page(1) # default to 1 when this view is triggered

    context = {
        'lh': transaction_page,
        'filter': lh,
    }

    if request.htmx:
        return render(request, 'tracker/partials/lichhoc-container.html', context)

    return render(request, 'tracker/lichhoc-list.html', context)

@login_required(login_url='/accounts/login/')
def search_lh(request):
    query = request.GET.get('search','')
    query_fr = request.GET.get('start_date',None)
    query_to = request.GET.get('end_date',None)
    #sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)
    print('searching: ' + query)
    #lh = Lichhoc.objects.all()
    lops = Lop.objects.filter(Q(ten__icontains=query))
    mhs = Monhoc.objects.filter(Q(ten__icontains=query))
    lmhs = LopMonhoc.objects.filter(lop__in=lops) | LopMonhoc.objects.filter(monhoc__in=mhs)
    lh = Lichhoc.objects.filter(lmh__in=lmhs)
    if query_fr:
        lh = lh.filter(thoigian__gte=query_fr)
    if query_to:
        lh = lh.filter(thoigian__lte=query_to)
    #lh = lh.filter(lmh__monhoc__ten__contains=query)
    paginator = Paginator(lh, 20)
    transaction_page = paginator.page(1) # default to 1 when this view is triggered

    context = {
        'lh': transaction_page,
        'filter': lh,
        'query_fr': query_fr,
        'query_to': query_to,
        'query': query
    }

    return render(request, 'tracker/partials/lichhoc-container.html', context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'message': "Transaction was added successfully!"}
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {'form': form}
            response = render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')

    context = {'form': TransactionForm()}
    return render(request, 'tracker/partials/create-transaction.html', context)

@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context = {'message': "Transaction was updated successfully!"}
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {
                'form': form,
                'transaction': transaction,
            }
            response = render(request, 'tracker/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')
        
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction,
    }
    return render(request, 'tracker/partials/update-transaction.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {
        'message': f"Transaction of {transaction.amount} on {transaction.date} was deleted successfully!"
    }
    return render(request, 'tracker/partials/transaction-success.html', context)

@login_required
def get_transactions(request):
    page = request.GET.get('page', 1)  # ?page=2
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    context = {
        'transactions': paginator.page(page)
    }
    return render(
        request,
        'tracker/partials/transactions-container.html#transaction_list',
        context
    )

@login_required(login_url='/accounts/login/')
def get_lichhoc(request):
    query = request.GET.get('search','')
    #sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)
    print('searching: ' + query)
    query_fr = request.GET.get('start_date',None)
    query_to = request.GET.get('end_date',None)
    #lh = Lichhoc.objects.all()
    lops = Lop.objects.filter(Q(ten__icontains=query))
    mhs = Monhoc.objects.filter(Q(ten__icontains=query))
    lmhs = LopMonhoc.objects.filter(lop__in=lops) | LopMonhoc.objects.filter(monhoc__in=mhs)
    lh = Lichhoc.objects.filter(lmh__in=lmhs)
    #lh = lh.filter(lmh__monhoc__ten__contains=query)

    if query_fr:
        lh = lh.filter(thoigian__gte=query_fr)
    if query_to:
        lh = lh.filter(thoigian__lte=query_to)

    page = request.GET.get('page', 1)  # ?page=2

    #lh = Lichhoc.objects.all()
    paginator = Paginator(lh, 20)
    context = {
        'lh': paginator.page(page)
    }
    return render(
        request,
        'tracker/partials/lichhoc-container.html#lichhoc_list',
        context
    )

def transaction_charts(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    income_expense_bar = plot_income_expenses_bar_chart(transaction_filter.qs)

    category_income_pie = plot_category_pie_chart(
        transaction_filter.qs.filter(type='income')
    )
    category_expense_pie = plot_category_pie_chart(
        transaction_filter.qs.filter(type='expense')
    )

    context = {
        'filter': transaction_filter,
        'income_expense_barchart': income_expense_bar.to_html(),
        'category_income_pie': category_income_pie.to_html(),
        'category_expense_pie': category_expense_pie.to_html(),
    }
    if request.htmx:
        return render(request, 'tracker/partials/charts-container.html', context)
    return render(request, 'tracker/charts.html', context)

@login_required
def export(request):
    if request.htmx:
        return HttpResponse(headers={'HX-Redirect': request.get_full_path()})
    
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    data = TransactionResource().export(transaction_filter.qs)
    response = HttpResponse(data.csv)
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    return response

@login_required
def import_transactions(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        resource = TransactionResource()
        dataset = Dataset()
        dataset.load(file.read().decode(), format='csv')
        result = resource.import_data(dataset, user=request.user, dry_run=True)

        for row in result:
            for error in row.errors:
                print(error)

        if not result.has_errors():
            resource.import_data(dataset, user=request.user, dry_run=False)
            context = {'message': f'{len(dataset)} transactions were uploaded successfully'}
        else:
            context = {'message': 'Sorry, an error occurred.'}
        return render(request, 'tracker/partials/transaction-success.html', context)
    return render(request, 'tracker/partials/import-transaction.html')