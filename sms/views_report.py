from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Lop, Ctdt, Hssv, Hsgv, SvStatus, HocphiStatus, LopMonhoc, Trungtam
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib.auth import get_user_model
from django.db.models import Sum

import psycopg2
import openpyxl, xlsxwriter 
import shutil, os

from django.conf import settings
from django.http import HttpResponse, Http404


User = get_user_model()

from django.shortcuts import render, get_object_or_404, redirect
from .models import Ctdt, Diemthanhphan, Hocky, HocphiStatus, Loaidiem, TeacherInfo, Hsgv, Hssv, CtdtMonhoc, Monhoc, Lop, Lichhoc, Hs81, Diemdanh, Diemthanhphan, Hocphi, LopMonhoc, DiemdanhAll
from .models import LopHk, Hp81, Ttgv, UploadedFile
from .forms import CreateDiem, CreateLichhoc, CreateLopMonhoc, CreateTeacher, CreateCtdtMonhoc, CreateDiemdanh, CreateHocphi, CreateCtdt, CreateLop, CreateSv, CreateGv
from .forms import CreateHp81, CreateTtgv,CreateUploadFile
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pandas as pd
from django.http import HttpResponseForbidden,HttpResponse

@login_required
def report_hs81(request):
    lh = None
    query_tt = None
    query_lop = None
    if request.method == "POST":
        query_lop = request.POST.get('lop', None)
        query_tt = request.POST.get('trungtam', None)
        lh = Lop.objects.all().order_by("ten").select_related("trungtam")
        if query_tt:
            lh = lh.filter(trungtam__ten__contains=query_tt.strip())
        if query_lop:
            lh = lh.filter(ten__contains=query_lop.strip())     

        #svs = Hssv.objects.filter(malop__in=lh).select_related("malop").order_by("malop", "msv")
        for l in lh:
            svs = Hssv.objects.filter(malop_id=l.id).order_by("msv")
            for sv in svs:
                sv.hp81 = Hp81.objects.filter(sv=sv).order_by("hk")
            l.svs = svs
        messages.success(request, "Tìm kiếm thành công!")
        paginator = Paginator(lh, 1)
        page = request.GET.get('page')
        lh = paginator.get_page(page)
    context = {
        "lh": lh,
        "query_tt": query_tt,
        "query_lop": query_lop
    }
    return render(request, "sms/report_hs81.html", context)

@login_required
def export_hs81(request, query_tt, query_lop):
    import pandas as pd

    mylist = []

    lh = Lop.objects.all().order_by("ten").select_related("trungtam")
    if query_tt:
        lh = lh.filter(trungtam__ten__contains=query_tt.strip())
    if query_lop:
        lh = lh.filter(ten__contains=query_lop.strip())     

    #svs = Hssv.objects.filter(malop__in=lh).select_related("malop").order_by("malop", "msv")
    for l in lh:
        #gvs = l.values()
        data={"Mã":"","Tên":l.ten, "Học kỳ":"","Hồ sơ":"","Học phí":"","Số tiền được giải ngân":"","Số tiền trường nhận":""}
        mylist.append(data)

        svs = Hssv.objects.filter(malop_id=l.id).order_by("msv")
        for sv in svs:
            data={"Mã":sv.msv,"Tên":sv.hoten, "Học kỳ":"","Hồ sơ":"","Học phí":"","Số tiền được giải ngân":"","Số tiền trường nhận":""}
            mylist.append(data)
            hp81s = Hp81.objects.filter(sv=sv).order_by("hk")
            for hp in hp81s:
                data={"Mã":"","Tên":"", "Học kỳ":hp.hk,"Hồ sơ": hp.hs81_st,"Học phí": hp.status,"Số tiền được giải ngân":hp.sotien1,"Số tiền trường nhận":hp.sotien2}
                mylist.append(data)


    df = pd.DataFrame(mylist)

    # Define the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=export_hs81-hp.xlsx'

    # Use Pandas to write the DataFrame to an Excel file
    df.to_excel(response, index=True, engine='openpyxl')

    return response

@login_required
def report_ttgv(request):
    lh = None
    query_tt = None
    query_lop = None
    if request.method == "POST":
        query_lop = request.POST.get('lop', None)
        query_tt = request.POST.get('trungtam', None)
        lh = Lop.objects.all().order_by("ten").select_related("trungtam")
        if query_tt:
            lh = lh.filter(trungtam__ten__contains=query_tt.strip())
        if query_lop:
            lh = lh.filter(ten__contains=query_lop.strip())     

        #svs = Hssv.objects.filter(malop__in=lh).select_related("malop").order_by("malop", "msv")
        for l in lh:
            lmhs = LopMonhoc.objects.filter(lop_id=l.id).select_related("monhoc").order_by("ngaystart")
            for lmh in lmhs:
                lmh.ttgvs = Ttgv.objects.filter(lopmh_id=lmh.id).select_related("gv").order_by("gv_id")
            l.lmhs = lmhs

        messages.success(request, "Tìm kiếm thành công!")
        paginator = Paginator(lh, 1)
        page = request.GET.get('page')
        lh = paginator.get_page(page)
    context = {
        "lh": lh,
        "query_tt": query_tt,
        "query_lop": query_lop
    }
    return render(request, "sms/report_ttgv.html", context)

@login_required
def report_kqht(request):
    lh = None
    query_tt = None
    query_lop = None
    if request.method == "POST":
        query_lop = request.POST.get('lop', None)
        query_tt = request.POST.get('trungtam', None)
        lh = Lop.objects.all().order_by("ten").select_related("trungtam")
        if query_tt:
            lh = lh.filter(trungtam__ten__contains=query_tt.strip())
        if query_lop:
            lh = lh.filter(ten__contains=query_lop.strip())     

        #svs = Hssv.objects.filter(malop__in=lh).select_related("malop").order_by("malop", "msv")
        for l in lh:
            lmhs = LopMonhoc.objects.filter(lop_id=l.id).select_related("monhoc").order_by("ngaystart")
            for lmh in lmhs:
                svs = Hssv.objects.filter(malop_id=l.id)
                lmh.diems = Diemthanhphan.objects.filter(monhoc_id=lmh.monhoc.id, status =1, sv_id__in= svs.values_list('id', flat=True)).select_related("sv","tp").order_by("sv_id", "tp_id")
            l.lmhs = lmhs

        messages.success(request, "Tìm kiếm thành công!")
        paginator = Paginator(lh, 1)
        page = request.GET.get('page')
        lh = paginator.get_page(page)
    context = {
        "lh": lh,
        "query_tt": query_tt,
        "query_lop": query_lop
    }
    return render(request, "sms/report_kqht.html", context)
