from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, F, Sum, Avg
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render

from shop.models import Purchase, RawRP
from shop.charts import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict
from sms.models import Lop, Hocky
from django.contrib.auth.decorators import login_required, permission_required

#@staff_member_required
def get_filter_options(request):
    grouped_purchases = Purchase.objects.annotate(year=ExtractYear("time")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


#@staff_member_required
def get_sales_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)
    grouped_purchases = purchases.annotate(price=F("item__price")).annotate(month=ExtractMonth("time"))\
        .values("month").annotate(average=Sum("item__price")).values("month", "average").order_by("month")

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })


#@staff_member_required
def spend_per_customer_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)
    grouped_purchases = purchases.annotate(price=F("item__price")).annotate(month=ExtractMonth("time"))\
        .values("month").annotate(average=Avg("item__price")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })


#@staff_member_required
def payment_success_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)

    return JsonResponse({
        "title": f"Payment success rate in {year}",
        "data": {
            "labels": ["Successful", "Unsuccessful"],
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": [colorSuccess, colorDanger],
                "borderColor": [colorSuccess, colorDanger],
                "data": [
                    purchases.filter(successful=True).count(),
                    purchases.filter(successful=False).count(),
                ],
            }]
        },
    })


#@staff_member_required
def payment_method_chart(request, year):
    purchases = Purchase.objects.filter(time__year=year)
    grouped_purchases = purchases.values("payment_method").annotate(count=Count("id"))\
        .values("payment_method", "count").order_by("payment_method")

    payment_method_dict = dict()

    for payment_method in Purchase.PAYMENT_METHODS:
        payment_method_dict[payment_method[1]] = 0

    for group in grouped_purchases:
        payment_method_dict[dict(Purchase.PAYMENT_METHODS)[group["payment_method"]]] = group["count"]

    return JsonResponse({
        "title": f"Payment method rate in {year}",
        "data": {
            "labels": list(payment_method_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": generate_color_palette(len(payment_method_dict)),
                "borderColor": generate_color_palette(len(payment_method_dict)),
                "data": list(payment_method_dict.values()),
            }]
        },
    })

@login_required
def ctdt_chart(request):
    query = """
                select c.id as id, c.ten as labels, count(s.id) as data from sms_ctdt c
                inner join sms_lop l
                    on l.ctdt_id = c.id
                inner join sms_hssv s
                    on s.lop_id = l.id
                group by c.id
                order by c.id
            """

    ctdts = RawRP.objects.raw(query)

    ctdt_dict = dict()

    for ctdt in ctdts:
        ctdt_dict[ctdt.labels] = ctdt.data

    return JsonResponse({
        "title": f"Số học viên phân theo Chương trình đào tạo",
        "data": {
            "labels": list(ctdt_dict.keys()),
            "datasets": [{
                "label": "Số người",
                "backgroundColor": generate_color_palette(len(ctdt_dict)),
                "borderColor": generate_color_palette(len(ctdt_dict)),
                "data": list(ctdt_dict.values()),
            }]
        },
    })

@login_required
def hs_chart(request, lop, hk):
    query = """
                select max(sv.id) as id, coalesce(hs.status,'Chưa nhập dữ liệu') as labels,count(coalesce(hs.status,'Chưa nhập dữ liệu')) as data from sms_hssv sv
                left outer join public.sms_hs81 hs
                    on sv.id = hs.sv_id and hs.hk_id=%s and sv.lop_id=%s
                group by hs.status
            """

    ctdts = RawRP.objects.raw(query,[hk, lop] )

    ctdt_dict = dict()

    for ctdt in ctdts:
        ctdt_dict[ctdt.labels] = ctdt.data

    return JsonResponse({
        "title": f"Số học viên phân theo Chương trình đào tạo",
        "data": {
            "labels": list(ctdt_dict.keys()),
            "datasets": [{
                "label": "Số người",
                "backgroundColor": generate_color_palette(len(ctdt_dict)),
                "borderColor": generate_color_palette(len(ctdt_dict)),
                "data": list(ctdt_dict.values()),
            }]
        },
    })

@login_required
def hp_chart(request, lop, hk):
    query = """
                select max(sv.id) as id, coalesce(hp.ten,'Chưa nhập dữ liệu') as labels, count(hp.*) as data
					from sms_hssv sv
                left outer join 
                    (select sv_id, hk_id, st.ten from public.sms_hp81
                    inner join public.sms_hocphistatus st
                        on status_id = st.id) as hp
                    on sv.id = hp.sv_id and hp.hk_id=%s and sv.lop_id=%s
				 group by hp.ten
            """

    ctdts = RawRP.objects.raw(query,[hk, lop] )

    ctdt_dict = dict()

    for ctdt in ctdts:
        ctdt_dict[ctdt.labels] = ctdt.data

    return JsonResponse({
        "title": f"Số học viên phân theo Chương trình đào tạo",
        "data": {
            "labels": list(ctdt_dict.keys()),
            "datasets": [{
                "label": "Số người",
                "backgroundColor": generate_color_palette(len(ctdt_dict)),
                "borderColor": generate_color_palette(len(ctdt_dict)),
                "data": list(ctdt_dict.values()),
            }]
        },
    })

@login_required
def lopsv_chart(request):
    query = """
                select max(l.id) as id, max(tt.ten) as labels, count(s.id) as data 
                from sms_lop l
                inner join sms_trungtam tt
                    on tt.id = l.trungtam_id
                inner join sms_hssv s
                    on s.lop_id = l.id
                group by l.trungtam_id
                order by l.trungtam_id       
            """

    ctdts = RawRP.objects.raw(query)

    ctdt_dict = dict()

    for ctdt in ctdts:
        ctdt_dict[ctdt.labels] = ctdt.data

    return JsonResponse({
        "title": f"Số học viên phân theo lớp",
        "data": {
            "labels": list(ctdt_dict.keys()),
            "datasets": [{
                "label": "Số người",
                "backgroundColor": generate_color_palette(len(ctdt_dict)),
                "borderColor": generate_color_palette(len(ctdt_dict)),
                "data": list(ctdt_dict.values()),
            }]
        },
    })
@login_required
@permission_required('dashboard.view_dashboard',raise_exception=True)
def statistics_view(request):
    lops = Lop.objects.all()
    hks = Hocky.objects.all()
    context = {
        "lops": lops,
        "hks": hks
    }
    return render(request, "statistics.html", context)
