from django.http import JsonResponse
#from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from django.shortcuts import render
from dashboard.models import DiemdanhRP, ChamcongRP, HocphiRP
from sms.models import Hssv, Location, House, Renter, HouseRenter, Hoadon
from django.core import serializers

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta


def dashboard_with_pivot(request):
    return render(request, 'dashboard/dashboard_with_pivot.html', {})

def pivot_data(request):
    query = """SELECT dd.id, sv.lop, mh.ten as monhoc, sv.hoten as sv, lh.thoigian, 1 as solan 
                    FROM public.teachers_diemdanh as dd
                inner join public.teachers_lichhoc as lh
                    on dd.lichhoc_id = lh.id
                inner join public.teachers_monhoc as mh
                    on lh.monhoc_id = mh.id
                inner join public.teachers_hssv as sv
                    on dd.sv_id = sv.id
                ORDER BY sv.lop ASC, sv.hoten"""
    dataset = DiemdanhRP.objects.raw(query)
    print(dataset)
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

@login_required
def report_diemdanh(request):
    query = """SELECT dd.id, sv.lop, mh.ten as monhoc, sv.hoten as sv, lh.thoigian 
                    FROM public.sms_diemdanh as dd
                inner join public.sms_lichhoc as lh
                    on dd.lichhoc_id = lh.id and dd.status = 0
                inner join public.sms_monhoc as mh
                    on lh.monhoc_id = mh.id
                inner join public.sms_hssv as sv
                    on dd.sv_id = sv.id
                ORDER BY sv.lop ASC, sv.hoten"""
    dd = DiemdanhRP.objects.raw(query)
    paginator = Paginator(dd, 10)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students
    }
    return render(request, "dashboard/report_diemdanh_chart1.html", context)

@login_required
def report_chamcong(request):
    query = """SELECT lh.id, gv.hoten as ten, l.ten as lop, mh.ten as monhoc, lh.thoigian, lh.sogio
                    FROM public.teachers_lichhoc as lh
                inner join public.teachers_hsgv as gv
                    on lh.giaovien_id = gv.id
                inner join public.teachers_monhoc as mh
                    on lh.monhoc_id = mh.id
                inner join public.teachers_lop as l
                    on lh.lop_id = l.id
                ORDER BY gv.hoten"""
    cc = ChamcongRP.objects.raw(query)
    paginator = Paginator(cc, 10)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students
    }
    return render(request, "dashboard/report_chamcong.html", context)


@login_required
def report_hocphi(request):
    query = """select sv.id, sv.hoten, sv.lop, hp.status, hp.sotien from teachers_hssv sv
                full outer join teachers_hocphi hp
	                on sv.id = hp.sv_id
                order by sv.lop, sv.id, hp.id"""

    cc = HocphiRP.objects.raw(query)
    if request.method == "POST":
            query_name = request.POST.get('name', None)
            if query_name:
                #lop_id = Lop.objects.get(ten = query_name).id
                query_name1 = "%" +query_name + "%"
                query = '''select sv.id, sv.hoten, sv.lop, hp.hk, hp.status, hp.sotien from teachers_hssv sv
                            full outer join teachers_hocphi hp
	                            on sv.id = hp.sv_id
                            where sv.lop like %s
                            order by sv.lop, sv.id, hp.id'''
                print(query)
                cc = HocphiRP.objects.raw(query, [query_name1])
                messages.success(request, "Ket qua tim kiem: " + query_name)

    paginator = Paginator(cc, 50)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students
    }
    return render(request, "dashboard/report_hocphi.html", context)

@login_required
@action(detail=False, methods=['get'], url_path='api-hssv')
def api_hssv(request):
    stud_lst = Hssv.objects.all()
    years = []
    for stu in stud_lst:
        years.append(stu.namsinh.year)
    #print(years)
    years = list(set(years))
    years.sort()
    data = []
    for year in years:
        data.append({
            'year': str(year),
            'count': Hssv.objects.all().count()
        })
    print(data)
    return Response(data, status=status.HTTP_200_OK)
    #return JsonResponse(data=data, status=404)
    #return JsonResponse(data)
    #return Response(data)


@login_required
def rental_dashboard(request):
    """Dashboard thống kê cho hệ thống cho thuê nhà"""
    
    # Thống kê tổng quan
    total_locations = Location.objects.count()
    total_houses = House.objects.count()
    total_renters = Renter.objects.count()
    active_contracts = HouseRenter.objects.filter(active=True).count()
    
    # Thống kê hóa đơn
    total_hoadon = Hoadon.objects.count()
    hoadon_chuatt = Hoadon.objects.filter(status='ChuaTT').count()
    hoadon_dangtt = Hoadon.objects.filter(status='DangTT').count()
    hoadon_datt = Hoadon.objects.filter(status='DaTT').count()
    hoadon_quahan = Hoadon.objects.filter(status='QuaHan').count()
    
    # Thống kê doanh thu
    total_revenue = Hoadon.objects.aggregate(
        total=Sum('TONG_CONG')
    )['total'] or 0
    
    total_paid = Hoadon.objects.aggregate(
        paid=Sum('SO_TIEN_DA_TRA')
    )['paid'] or 0
    
    total_debt = Hoadon.objects.aggregate(
        debt=Sum('CONG_NO')
    )['debt'] or 0
    
    # Thống kê theo tháng (6 tháng gần nhất)
    today = timezone.now()
    six_months_ago = today - timedelta(days=180)
    
    monthly_revenue = []
    monthly_labels = []
    for i in range(6):
        month_date = today - timedelta(days=30*i)
        month_start = month_date.replace(day=1)
        if i == 0:
            month_end = today
        else:
            next_month = month_start + timedelta(days=32)
            month_end = next_month.replace(day=1) - timedelta(days=1)
        
        revenue = Hoadon.objects.filter(
            ngay_tao__gte=month_start,
            ngay_tao__lte=month_end
        ).aggregate(total=Sum('TONG_CONG'))['total'] or 0
        
        monthly_revenue.insert(0, revenue)
        monthly_labels.insert(0, f"{month_start.month}/{month_start.year}")
    
    # Thống kê nhà trọ theo loại
    house_by_type = House.objects.values('loainha').annotate(count=Count('id'))
    house_type_labels = [item['loainha'] for item in house_by_type]
    house_type_data = [item['count'] for item in house_by_type]
    
    # Thống kê giá thuê trung bình
    avg_rent = House.objects.aggregate(avg=Avg('permonth'))['avg'] or 0
    
    # Hóa đơn sắp đến hạn (trong 7 ngày tới)
    upcoming_due = Hoadon.objects.filter(
        duedate__lte=today.date() + timedelta(days=7),
        duedate__gte=today.date(),
        status__in=['ChuaTT', 'DangTT']
    ).count()
    
    context = {
        'total_locations': total_locations,
        'total_houses': total_houses,
        'total_renters': total_renters,
        'active_contracts': active_contracts,
        'total_hoadon': total_hoadon,
        'hoadon_chuatt': hoadon_chuatt,
        'hoadon_dangtt': hoadon_dangtt,
        'hoadon_datt': hoadon_datt,
        'hoadon_quahan': hoadon_quahan,
        'total_revenue': total_revenue,
        'total_paid': total_paid,
        'total_debt': total_debt,
        'monthly_revenue': monthly_revenue,
        'monthly_labels': monthly_labels,
        'house_type_labels': house_type_labels,
        'house_type_data': house_type_data,
        'avg_rent': avg_rent,
        'upcoming_due': upcoming_due,
    }
    
    return render(request, 'dashboard/rental_dashboard.html', context)