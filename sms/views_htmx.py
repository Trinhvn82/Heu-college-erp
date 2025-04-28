from django.shortcuts import render, get_object_or_404, redirect

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


@login_required
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

@login_required
def search_lh(request):
    if not request.user.is_authenticated:
        return redirect("login")
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

