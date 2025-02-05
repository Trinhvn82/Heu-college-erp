from django.http import JsonResponse
#from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from django.shortcuts import render
from dashboard.models import DiemdanhRP, ChamcongRP, HocphiRP
from sms.models import Hssv
from django.core import serializers

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


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