from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Lop, Ctdt, Hssv, Hsgv, SvStatus, HocphiStatus, LopMonhoc, Trungtam, NsLop
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
from .models import LopHk, Hp81, Ttgv, UploadedFile, Phong, Hsns
from .forms import CreateDiem, CreateLichhoc, CreateLopMonhoc, CreateTeacher, CreateCtdtMonhoc, CreateDiemdanh, CreateHocphi, CreateCtdt, CreateLop, CreateSv, CreateGv
from .forms import CreateHp81, CreateTtgv,CreateUploadFile, CreateNs
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pandas as pd
from django.http import HttpResponseForbidden,HttpResponse


#@login_required
def index(request):
    #if request.user.is_teacher:
    #if request.user:
        #return render(request, 'sms/lop-list.html')
    return redirect("shop-statistics")
    #return render(request, 'info/logout.html')

# Teacher Views

@login_required
def t_clas(request, teacher_id, choice):
    teacher1 = get_object_or_404(Hsgv, id=teacher_id)
    return render(request, 'info/t_clas.html', {'teacher1': teacher1, 'choice': choice})


@login_required()
def t_timetable(request, teacher_id):
    #asst = AssignTime.objects.filter(assign__teacher_id=teacher_id)
    class_matrix = [[True for i in range(12)] for j in range(6)]

    '''
    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(12):
            if j == 0:
                class_matrix[i][0] = d[0]
                continue
            if j == 4 or j == 8:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                class_matrix[i][j] = a
            except AssignTime.DoesNotExist:
                pass
            t += 1
    '''
    context = {
        'class_matrix': class_matrix,
    }
    return render(request, 'sms/t_timetable.html', context)


# Create your views here.
def teacher_list(request):
    teachers = TeacherInfo.objects.all()

    paginator = Paginator(teachers, 10)
    page = request.GET.get('page')
    paged_teachers = paginator.get_page(page)
    context = {
        "teachers": paged_teachers
    }
    return render(request, "sms/teacher_list.html", context)

@login_required
def gv_list(request):
    teachers = Hsgv.objects.all().order_by('hoten')
    if request.method == "POST":
            query_name = request.POST.get('ten', None)
            if query_name:
                teachers = Hsgv.objects.filter(hoten__contains=query_name).order_by('hoten')
                messages.success(request, "Ket qua tim kiem voi ten co chua: " + query_name)
#                return render(request, 'product-search.html', {"results":results})

    paginator = Paginator(teachers, 20)
    page = request.GET.get('page')
    paged_teachers = paginator.get_page(page)
    context = {
        "teachers": paged_teachers
    }
    return render(request, "sms/gv_list.html", context)

@login_required
def ns_list(request):
    ns = Hsns.objects.all().order_by('hoten')
    if request.method == "POST":
            query_name = request.POST.get('ten', None)
            if query_name:
                ns = Hsns.objects.filter(hoten__contains=query_name).order_by('hoten')
                messages.success(request, "Ket qua tim kiem voi ten co chua: " + query_name)
#                return render(request, 'product-search.html', {"results":results})

    paginator = Paginator(ns, 20)
    page = request.GET.get('page')
    paged_ns = paginator.get_page(page)
    context = {
        "nss": paged_ns
    }
    return render(request, "sms/ns_list.html", context)

@login_required
def sv_list(request):
    students = Hssv.objects.all().order_by('msv')
    if request.method == "POST":
            query_name = request.POST.get('ten', None)
            if query_name:
                students = Hssv.objects.filter(hoten__contains=query_name)
                messages.success(request, "Ket qua tim kiem voi ten co chua: " + query_name)
#                return render(request, 'product-search.html', {"results":results})

    paginator = Paginator(students, 20)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "students": paged_students
    }
    return render(request, "sms/sv_list.html", context)

@login_required
def sv_lop(request, lop_id):
    #students = Hssv.objects.all()
    tenlop = Lop.objects.get(id = lop_id).ten
    students = Hssv.objects.filter(malop_id = lop_id).order_by('msv')
    paginator = Paginator(students, 100)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    print("LOP ID la ")
    print(lop_id)

    context = {
        "students": paged_students,
        "lop_id": lop_id,
        "tenlop": tenlop
    }
    return render(request, "sms/svlop_list.html", context)

@login_required
def lichhoc_lop(request, lop_id):
    #students = Hssv.objects.all()
    tenlop = Lop.objects.get(id = lop_id).ten
    lichhoc = Lichhoc.objects.filter(lop_id = lop_id)
    paginator = Paginator(lichhoc, 100)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students,
        "tenlop": tenlop
    }
    return render(request, "sms/lichhoc-lop_list.html", context)


@login_required
def lichhoc_lopmh(request, lopmh_id):
    #students = Hssv.objects.all()
    lmh = LopMonhoc.objects.filter(id = lopmh_id).select_related("monhoc", "lop")[0]
    lop_id = LopMonhoc.objects.get(id = lopmh_id).lop_id
    monhoc_id = LopMonhoc.objects.get(id = lopmh_id).monhoc_id
    lichhoc = Lichhoc.objects.filter(lop_id = lmh.lop_id, monhoc_id = lmh.monhoc_id).order_by('thoigian')
    paginator = Paginator(lichhoc, 100)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)

    #lmh = LopMonhoc.objects.get(id = lopmh_id).select_related("monhoc", "lop")

    context = {
        "lh": paged_students,
        "lopmh_id": lopmh_id,
        "lop_id": lmh.lop_id,
        "monhoc_id": lmh.monhoc_id,
        "monhoc": lmh.monhoc.ten
    }
    return render(request, "sms/lichhoc-lopmh_list.html", context)
@login_required
def hocphi_lop(request, lop_id):
    #students = Hssv.objects.all()
    tenlop = Lop.objects.get(id = lop_id).ten
    hocphi = Hocphi.objects.all().select_related("sv").filter(lop_id = lop_id)
    paginator = Paginator(hocphi, 100)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students,
        "tenlop": tenlop,
        "lop_id": lop_id
    }
    return render(request, "sms/hocphi-lop_list.html", context)
@login_required
def diem_lop(request, lop_id):

    #students = Hssv.objects.all()
    tenlop = Lop.objects.get(id = lop_id).ten
    diems = Diemthanhphan.objects.all().select_related("sv", "tp", "monhoc").filter(sv__lop__contains=tenlop)
    if request.method == "POST":
            query_name = request.POST.get('name', None)
            if query_name:
                diems = Diemthanhphan.objects.all().select_related("sv", "tp", "monhoc").filter(sv__lop__contains=tenlop, sv__hoten__contains=query_name)
                #students = Hssv.objects.filter(hoten__contains=query_name)
                messages.success(request, "Ket qua tim kiem voi ten co chua: " + query_name)
#                return render(request, 'product-search.html', {"results":results})
    #lichhoc = Diemthanhphan.objects.filter(lop_id = lop_id)
    paginator = Paginator(diems, 40)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "diems": paged_students,
        "tenlop": tenlop,
        "lop_id": lop_id
    }
    return render(request, "sms/diem-lop_list.html", context)

@login_required
def diem_lmh(request, lmh_id):

    #students = Hssv.objects.all()
    lop_id = LopMonhoc.objects.get(id = lmh_id).lop_id
    mh_id = LopMonhoc.objects.get(id = lmh_id).monhoc_id

    tenlop = Lop.objects.get(id = lop_id).ma
    tenmh = Monhoc.objects.get(id = mh_id).ten

    stud_list = Hssv.objects.filter(malop_id = lop_id)
    lds= Loaidiem.objects.all()
    diems = Diemthanhphan.objects.all().select_related("sv", "tp", "monhoc").filter(sv__in=stud_list, monhoc_id =mh_id).order_by('tp_id', 'sv_id')
    if request.method == "POST":
        for stud in stud_list:
            for ld in lds:
                id = "C"+str(stud.id)+"-"+str(ld.id)
                diem = request.POST[id]
                mark = Diemthanhphan.objects.get(sv_id = stud.id, tp_id = ld.id, monhoc_id=mh_id)
                mark.diem = diem
                mark.status = 1
                mark.save()
        messages.success(request, "Cap nhat diem thanh cong!")
        return redirect("lop_monhoc", lop_id)


    if not diems.first():
        #create mark record
        for stud in stud_list:
            for ld in lds:
                mark = Diemthanhphan(diem =0, sv_id = stud.id, tp_id = ld.id, monhoc_id=mh_id)
                mark.save()
        diems = Diemthanhphan.objects.all().select_related("sv", "tp", "monhoc").filter(sv__in=stud_list, monhoc_id =mh_id)

    context = {
        "diems": diems,
        "tenlop": tenlop,
        "tenmh": tenmh
    }
    return render(request, "sms/diem-lmh.html", context)

@login_required
def diem_lmh_lst(request, lmh_id):

    #students = Hssv.objects.all()
    lop_id = LopMonhoc.objects.get(id = lmh_id).lop_id
    mh_id = LopMonhoc.objects.get(id = lmh_id).monhoc_id

    tenlop = Lop.objects.get(id = lop_id).ma
    tenmh = Monhoc.objects.get(id = mh_id).ten
    lds= Loaidiem.objects.all()
    lol=[]
    diems = Diemthanhphan.objects.all()
    stud_list = Hssv.objects.filter(malop_id = lop_id)
    lds= Loaidiem.objects.all()
    for ld in lds:
        st = Diemthanhphan.objects.filter(sv__in=stud_list, monhoc_id =mh_id, tp_id=ld.ma, status = 1).first()
        if st:
            lol.append({ "ma":ld.ma,"ten": ld.ten, "st": 1})
        else:
            lol.append({ "ma":ld.ma,"ten": ld.ten, "st": 0})
    context = {
        "tenlop": tenlop,
        "lds": lds,
        "lmh_id":lmh_id,
        "lol":lol,
        "tenmh": tenmh
    }
    return render(request, "sms/diem-lmh-lst.html", context)

@login_required
def gv_lmh_lst(request, lmh_id):

    #lmh = LopMonhoc.objects.get(id = lmh_id)
    lmh = LopMonhoc.objects.filter(id = lmh_id).select_related("monhoc", "lop")[0]

    lh = Lichhoc.objects.filter(lop_id = lmh.lop_id, monhoc_id = lmh.monhoc_id).select_related("lop", "monhoc")
    gvs = Hsgv.objects.filter(id__in = lh.values_list('giaovien_id', flat=True))
    
    for gv in gvs:
        gv.lhs = Lichhoc.objects.filter(lop_id = lmh.lop_id, monhoc_id = lmh.monhoc_id, giaovien_id = gv.id)
        gv.sotiet = gv.lhs.aggregate(Sum('sotiet'))['sotiet__sum']
        if Ttgv.objects.filter(gv_id = gv.id, lopmh_id = lmh_id).exists():
            gv.sotien = Ttgv.objects.get(gv_id = gv.id, lopmh_id = lmh_id).sotien2
        else:
            gv.sotien = 0
        #Sale.objects.filter(type='Flour').aggregate(Sum('column'))['column__sum']
        
    context = {
        "lmh": lmh,
        "gvs": gvs,
    }
    return render(request, "sms/gv-lmh-lst.html", context)

@login_required
def details_gv(request, gv_id):

    #lmh = LopMonhoc.objects.get(id = lmh_id)
    lh = Lichhoc.objects.filter(giaovien_id = gv_id).select_related("lop", "monhoc")
    #lmh = LopMonhoc.objects.filter(id = lmh_id).select_related("monhoc", "lop")[0]

    lops = Lop.objects.filter(id__in = lh.values_list('lop_id', flat=True))
    #lmh = LopMonhoc.objects.filter(id__in = lh.values_list('monhoc_id', flat=True))
    gv = Hsgv.objects.get(id = gv_id)

    #gvs = Hsgv.objects.filter(id__in = lh.values_list('giaovien_id', flat=True))
    
    for l in lops:
        mhs = LopMonhoc.objects.filter(monhoc_id__in = lh.values_list('monhoc_id', flat=True), lop_id = l.id).select_related("monhoc")
        for mh in mhs:
            mh.lhs = Lichhoc.objects.filter(giaovien_id = gv_id, lop_id = l.id, monhoc_id = mh.monhoc_id)
            mh.sotiet = mh.lhs.aggregate(Sum('sotiet'))['sotiet__sum']
        l.mhs = mhs

        
    context = {
        "lops": lops,
        "gv": gv,
    }
    return render(request, "sms/gv_details.html", context)

@login_required
def lop81_lst(request, lop_id):

    tenlop = Lop.objects.get(id = lop_id).ma
    hks= Hocky.objects.all()

    lol=[]
    diems = Hs81.objects.all()
    stud_list = Hssv.objects.filter(malop_id = lop_id)
    hks= Hocky.objects.all()
    for hk in hks:
        ft1 = Hs81.objects.filter(lop_id=lop_id, hk= hk.ma,status = 1).first()
        ft2 = Hocphi.objects.filter(lop_id=lop_id, hk= hk.ma,status = 1).first()
        if ft1:
            st1=1
        else:
            st1=0
        if ft2:
            st2=1
        else:
            st2=0
        lol.append({ "ma":hk.ma,"ten": hk.ten, "st1": st1, "st2": st2})

    context = {
        "tenlop": tenlop,
        "lol": lol,
        "lop_id":lop_id
    }
    return render(request, "sms/lop81-lst.html", context)
@login_required
def diem_lmh_dtp(request, lmh_id, dtp_id):

    #students = Hssv.objects.all()
    lop_id = LopMonhoc.objects.get(id = lmh_id).lop_id
    mh_id = LopMonhoc.objects.get(id = lmh_id).monhoc_id

    tenlop = Lop.objects.get(id = lop_id).ma
    tenmh = Monhoc.objects.get(id = mh_id).ten

    stud_list = Hssv.objects.filter(malop_id = lop_id)
    lds= Loaidiem.objects.filter(ma=dtp_id)
    diems = Diemthanhphan.objects.all().select_related("sv", "tp", "monhoc").filter(sv__in=stud_list, monhoc_id =mh_id, tp_id=dtp_id).order_by('tp_id', 'sv_id')
    if request.method == "POST":
        for stud in stud_list:
            for ld in lds:
                id = "C"+str(stud.id)+"-"+str(ld.ma)
                diem = request.POST[id]
                mark = Diemthanhphan.objects.get(sv_id = stud.id, tp_id = ld.ma, monhoc_id=mh_id)
                mark.diem = diem
                mark.status = 1
                mark.save()
        messages.success(request, "Cap nhat diem thanh cong!")
        return redirect("lop_monhoc", lop_id)


    if not diems.first():
        #create mark record
        for stud in stud_list:
            for ld in lds:
                mark = Diemthanhphan(diem =0, sv_id = stud.id, tp_id = ld.ma, monhoc_id=mh_id)
                mark.save()
        diems = Diemthanhphan.objects.all().select_related("sv", "tp", "monhoc").filter(sv__in=stud_list, monhoc_id =mh_id, tp_id=dtp_id).order_by('tp_id', 'sv_id')

    context = {
        "diems": diems,
        "tenlop": tenlop,
        "lds": lds,
        "lmh_id":lmh_id,
        "tenmh": tenmh
    }
    return render(request, "sms/diem-lmh.html", context)
@login_required
def lop81_hk(request, lop_id, hk_ma):

    tenlop = Lop.objects.get(id = lop_id).ma
    hks= Hocky.objects.filter(ma=hk_ma)
    stud_list = Hssv.objects.filter(malop_id = lop_id)
    hss = Hs81.objects.all().select_related("sv").filter(sv__in=stud_list, hk=hk_ma).order_by('sv_id')
    if request.method == "POST":
        for stud in stud_list:
            for hk in hks:
                hs = Hs81.objects.get(sv_id = stud.id,hk=hk.ma)
                hs.dondn = request.POST["dondn"+str(stud.id)]
                hs.cntn = request.POST["cntn"+str(stud.id)]
                hs.bangtn = request.POST["bangtn"+str(stud.id)]
                hs.xnct = request.POST["xnct"+str(stud.id)]
                hs.cccd = request.POST["cccd"+str(stud.id)]
                hs.cccdbo = request.POST["cccdbo"+str(stud.id)]
                hs.cccdme = request.POST["cccdme"+str(stud.id)]
                hs.gks = request.POST["gks"+str(stud.id)]
                hs.ghichu = request.POST["ghichu"+str(stud.id)]
                hs.status = 1

                hs.save()
        messages.success(request, "Cap nhat ho so 81 thanh cong!")
        return redirect("lop81-lst", lop_id)


    if not hss.first():
        #create hs81 record
        for stud in stud_list:
            for hk in hks:
                hs = Hs81(sv_id = stud.id, lop_id = lop_id, hk=hk.ma)
                hs.save()
        hss = Hs81.objects.all().select_related("sv").filter(sv__in=stud_list, hk=hk_ma).order_by('sv_id')

    context = {
        "hss": hss,
        "tenlop": tenlop,
        "hk_ma": hk_ma
    }
    return render(request, "sms/lop81-hk.html", context)

@login_required
def lophp_hk(request, lop_id, hk_ma):

    tenlop = Lop.objects.get(id = lop_id).ma
    hks= Hocky.objects.filter(ma=hk_ma)
    st= HocphiStatus.objects.all()
    stud_list = Hssv.objects.filter(malop_id = lop_id)
    hps = Hocphi.objects.all().select_related("sv").filter(sv__in=stud_list, hk=hk_ma).order_by('sv_id')
    if request.method == "POST":
        for stud in stud_list:
            for hk in hks:
                hs = Hocphi.objects.get(sv_id = stud.id,hk=hk.ma,lop_id = lop_id)
                hs.hpstatus = request.POST["status"+str(stud.id)]
                hs.ghichu = request.POST["ghichu"+str(stud.id)]
                hs.status = 1
                hs.save()
        messages.success(request, "Cap nhat thong tin hoc phi thanh cong!")
        return redirect("lop81-lst", lop_id)


    if not hps.first():
        #create hoc phi record
        for stud in stud_list:
            for hk in hks:
                hp = Hocphi(sv_id = stud.id, lop_id = lop_id, hk=hk.ma)
                hp.save()
        hps = Hocphi.objects.all().select_related("sv").filter(sv__in=stud_list, hk=hk_ma).order_by('sv_id')

    context = {
        "hps": hps,
        "st": st,
        "tenlop": tenlop,
        "hk_ma": hk_ma
    }
    return render(request, "sms/lophp-hk.html", context)

@login_required
def ctdt_list(request):
    ctdt = Ctdt.objects.all()

    paginator = Paginator(ctdt, 20)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "ctdt": paged_students
    }
    return render(request, "sms/ctdt_list.html", context)

@login_required
def import_monhoc_dm(request):
    if request.method == "POST":
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        if 'mh-lst' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin mon hoc")
            #return redirect("ctdt_list")
        else:
            sheet = wb["mh-lst"]
            for r in range(4, sheet.max_row):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                chuongtrinh = sheet.cell(r,3).value
                sotinchi = sheet.cell(r,4).value
                sogio_lt = sheet.cell(r,5).value
                sogio_th = sheet.cell(r,6).value
                sogio_kt = sheet.cell(r,7).value
                if Monhoc.objects.filter(ma=ma, ten=ten, chuongtrinh=chuongtrinh).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    mh = Monhoc(ma=ma, ten=ten, chuongtrinh=chuongtrinh, sotinchi=sotinchi, sogio_lt=sogio_lt,sogio_th=sogio_th,sogio_kt=sogio_kt)
                    mh.save()

        if 'hk-lst' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin hoc ky")
            #return redirect("ctdt_list")
        else:

            sheet = wb["hk-lst"]
            for r in range(2, sheet.max_row+1):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                if Hocky.objects.filter(ma=ma).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    hk = Hocky(ma=ma, ten=ten)
                    hk.save()

        if 'ld-lst' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin loai diem")
            #return redirect("ctdt_list")
        else:

            sheet = wb["ld-lst"]
            for r in range(2, sheet.max_row+1):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                if Loaidiem.objects.filter(ma=ma).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    ld = Loaidiem(ma=ma, ten=ten)
                    ld.save()

        if 'hp-st' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin tinh trang hoc phi")
            #return redirect("ctdt_list")

        else:
            sheet = wb["hp-st"]
            for r in range(2, sheet.max_row+1):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                if HocphiStatus.objects.filter(ma=ma).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    hp = HocphiStatus(ma=ma, ten=ten)
                    hp.save()

        if 'sv-st' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin tinh trang sinh vien")
            #return redirect("ctdt_list")

        else:
            sheet = wb["sv-st"]
            for r in range(2, sheet.max_row+1):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                if SvStatus.objects.filter(ma=ma).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    hp = SvStatus(ma=ma, ten=ten)
                    hp.save()

        if 'tt-lst' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin danh sách trung tâm")
            #return redirect("ctdt_list")

        else:
            sheet = wb["tt-lst"]
            for r in range(2, sheet.max_row+1):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                if Trungtam.objects.filter(ma=ma).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    hp = Trungtam(ma=ma, ten=ten)
                    hp.save()

        if 'phong-lst' not in wb.sheetnames:
            messages.error(request, "File excel khong co thong tin danh sách phòng")
            #return redirect("ctdt_list")

        else:
            sheet = wb["phong-lst"]
            for r in range(2, sheet.max_row+1):
            #for r in range(sheet.max_row-1, sheet.max_row):
                ma = sheet.cell(r,1).value
                ten = sheet.cell(r,2).value
                if Phong.objects.filter(ma=ma).exists():
                    messages.error(request, 'Ma: ' + str(ma) + ' already exists')
                else:
                    hp = Phong(ma=ma, ten=ten)
                    hp.save()
        messages.success(request, "Import done!")
        return redirect("ctdt_list")
@login_required
def import_lopsv(request, lop_id):
    if request.method == "POST":
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        if 'lopsv' not in wb.sheetnames:
            messages.error(request, "File excel khong dung format")
            return redirect("svlop_list", lop_id)

        sheet = wb["lopsv"]
        #for r in range(3, sheet.max_row+1):
        #maxid=500
        #for r in range(3, 44):
        for r in range(3, sheet.max_row+1):
            #maxid = maxid+1
            v1 = sheet.cell(r,1).value
            v2 = sheet.cell(r,2).value
            v3 = sheet.cell(r,3).value
            v4 = sheet.cell(r,4).value
            v5 = sheet.cell(r,5).value
            #v6 = sheet.cell(r,6).value
            #v7 = sheet.cell(r,7).value
            #v8 = sheet.cell(r,8).value
            v9 = sheet.cell(r,9).value
            #v10 = sheet.cell(r,10).value
            #v11 = sheet.cell(r,11).value
            #v12 = sheet.cell(r,12).value
            v13 = sheet.cell(r,13).value
            v14 = sheet.cell(r,14).value
            v15 = sheet.cell(r,15).value
            v16 = sheet.cell(r,16).value
            v17 = sheet.cell(r,17).value
            v18 = sheet.cell(r,18).value
            #print(type(v4))
            if Hssv.objects.filter(msv=v1).exists():
                messages.error(request, 'Mã: ' + v1+ ' already exists')
            elif type(v4) is not datetime:
                messages.error(request, 'Mã: ' + v1 + ' Namsinh: ' + v4 + ' not in date format')
            else:
                sv = Hssv(msv=v1, hoten = v2, lop = v3, namsinh=v4, gioitinh=v5, diachi=v9, cccd=v13, hotenbo=v14, hotenme=v15,sdths=v16, sdtph=v17, ghichu=v18, malop_id=lop_id)
                sv.save()

        messages.success(request, "Import thanh cong!")
        return redirect("svlop_list", lop_id)

@login_required
def import_gv(request):
    if request.method == "POST":
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheets = wb.sheetnames
        print(sheets)
        #if 'hsgv' not in wb.sheetnames:
        #    messages.error(request, "File excel khong dung format hsgv")
        #    return redirect("gv_list")
        sheet = wb["hsgv"]
        for r in range(2, sheet.max_row+1):
            ma = sheet.cell(r,1).value
            email = sheet.cell(r,2).value
            hoten = sheet.cell(r,3).value
            diachi = sheet.cell(r,4).value
            quequan = sheet.cell(r,5).value
            sdt = sheet.cell(r,6).value
            gioitinh = sheet.cell(r,7).value
            cccd = sheet.cell(r,8).value
            tthn = sheet.cell(r,9).value
            dantoc = sheet.cell(r,10).value
            loaihd = sheet.cell(r,11).value
            hocham = sheet.cell(r,12).value
            hocvi = sheet.cell(r,13).value
            stk = sheet.cell(r,14).value
            bank = sheet.cell(r,15).value
            branch = sheet.cell(r,16).value
            if Hsgv.objects.filter(ma=ma).exists():
                messages.error(request, 'Ma: ' + ma + ' already exists')
            else:
                gv = Hsgv(ma=ma, email=email, hoten=hoten, diachi=diachi, 
                        quequan=quequan, sdt=sdt, gioitinh=gioitinh, cccd=cccd, tthn=tthn)
                gv.save()

        messages.success(request, "Import thanh cong!")
        return redirect("gv_list")

@login_required
def import_ns(request):
    if request.method == "POST":
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheets = wb.sheetnames
        print(sheets)
        #if 'hsgv' not in wb.sheetnames:
        #    messages.error(request, "File excel khong dung format hsgv")
        #    return redirect("gv_list")
        sheet = wb["hsns"]
        for r in range(2, sheet.max_row+1):
            ma = sheet.cell(r,1).value
            email = sheet.cell(r,2).value
            hoten = sheet.cell(r,3).value
            diachi = sheet.cell(r,4).value
            quequan = sheet.cell(r,5).value
            sdt = sheet.cell(r,6).value
            gioitinh = sheet.cell(r,7).value
            cccd = sheet.cell(r,8).value
            if Hsns.objects.filter(ma=ma).exists():
                messages.error(request, 'Ma: ' + ma + ' already exists')
            else:
                ns = Hsns(ma=ma, email=email, hoten=hoten, diachi=diachi, 
                        quequan=quequan, sdt=sdt, gioitinh=gioitinh, cccd=cccd)
                ns.save()

        messages.success(request, "Import thanh cong!")
        return redirect("ns_list")

@login_required
def export_gv(request):
    # Query the Person model to get all records
    gvs = Hsgv.objects.all().values()
    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame(list(gvs))

    # Define the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=giaovien.xlsx'

    # Use Pandas to write the DataFrame to an Excel file
    df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required
def export_sv(request):
    # Query the Person model to get all records
    gvs = Hssv.objects.all().values()
    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame(list(gvs))

    # Define the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=hocvien.xlsx'

    # Use Pandas to write the DataFrame to an Excel file
    df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required
def export_lh(request):
    # Query the Person model to get all records
    gvs = Lichhoc.objects.all().values()
    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame(list(gvs))

    # Define the Excel file response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=lichhoc.xlsx'

    # Use Pandas to write the DataFrame to an Excel file
    df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required
def lop_list(request):
    #if not request.user.username:
    #    messages.error(request, "Login required")
    #    return redirect("login")
    #from django.contrib.auth.models import User

    #user = User.objects.all()
    #user = User.objects.create_user(username='john',
    #                             email='jlennon@beatles.com',
    #                             password='glass onion')
    lop = Lop.objects.all().select_related("ctdt").order_by('id')
    print(Lop.history.all())
    #print(request.user.username)
    paginator = Paginator(lop, 20)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lop": paged_students
    }
    return render(request, "sms/lop_list.html", context)

@login_required
def lichhoc_list(request):
    lh = Lichhoc.objects.all().select_related("lop", "monhoc").order_by('thoigian')
    if request.method == "POST":
            query_lop = request.POST.get('lop', None)
            query_mh = request.POST.get('monhoc', None)
            query_tgian1 = request.POST.get('tgian1', None)
            query_tgian2 = request.POST.get('tgian2', None)
            if query_lop:
                lh = lh.filter(lop__ten__contains=query_lop)     
            if query_mh:
                lh = lh.filter(monhoc__ten__contains=query_mh)     
            if query_tgian1:
                lh = lh.filter(thoigian__gte=query_tgian1)     
            if query_tgian2:
                lh = lh.filter(thoigian__lte=query_tgian2)     
            messages.success(request, "Tìm kiếm thành công!")
    paginator = Paginator(lh, 20)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students
    }
    return render(request, "sms/lichhoc_list.html", context)

@login_required
def diemdanh_list(request, lh_id):
    lh = Diemdanh.objects.all().select_related("sv", "lichhoc").filter(lichhoc_id=lh_id)
    ttlh = Lichhoc.objects.all().select_related("lop", "monhoc").get(id = lh_id)
    paginator = Paginator(lh, 50)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "lh": paged_students,
        "ttlh": ttlh

    }
    return render(request, "sms/lichhoc-diemdanh_list.html", context)

@login_required
def diemdanh_lop(request, lh_id):
    ttlh = Lichhoc.objects.get(id = lh_id)
    svlop = Hssv.objects.filter(malop_id = ttlh.lop_id)
    dds = Diemdanh.objects.filter(lichhoc_id = lh_id).order_by('sv_id')
    lmh = LopMonhoc.objects.get(lop_id = ttlh.lop_id, monhoc_id =ttlh.monhoc_id).id
    #sv = Hssv.objects.filter(malop_id = ttlh.lop_id)
    if request.method == "POST":
        for stud in svlop:
            id = "C"+str(stud.id)
            status = request.POST[id]
            dd = Diemdanh.objects.get(lichhoc_id = lh_id, sv_id=stud.id)
            dd.status=status
            dd.save()
        #ttlh.status=1
        #ttlh.save()
        messages.success(request, "Cap nhat diem danh thanh cong!")
        return redirect("lichhoclopmh_list", lmh)


    for stud in svlop:
        if not Diemdanh.objects.filter(sv_id = stud.id, lichhoc_id = lh_id).first():
            dd = Diemdanh(sv_id = stud.id, lichhoc_id = lh_id, status=1)
            dd.save()

    dds = Diemdanh.objects.select_related("sv").filter(lichhoc_id = lh_id).order_by('sv_id')
    context = {
        "dds": dds,
        "lh_id": lh_id,
        "lmh": lmh,
        "ttlh": ttlh
    }
    return render(request, "sms/diemdanh.html", context)

@login_required
def ctdt_monhoc(request, ctdt_id):
    mhs = Monhoc.objects.all()
    cms = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id).order_by('monhoc_id')
    if request.method == "POST":
        for mh in cms:
            id = "C"+str(mh.id)
            status = request.POST[id]
            print(id)
            print(status)
            cm = CtdtMonhoc.objects.get(id = mh.id)
            cm.status=status
            cm.save() 
        #     id = "C"+str(stud.id)
        #     status = request.POST[id]
        #     dd = Diemdanh.objects.get(lichhoc_id = lh_id, sv_id=stud.id)
        #     dd.status=status
        #     dd.save() 
        # ttlh.status=1
        # ttlh.save()
        messages.success(request, "Cập nhật môn học thành công!")
        return redirect("ctdt_list")


    for mh in mhs:
        if not CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, monhoc_id = mh.id).first():
            dd = CtdtMonhoc(ctdt_id = ctdt_id, monhoc_id = mh.id, hocky=1)
            dd.save()

    cms = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id).select_related("monhoc").order_by('monhoc_id')
    context = {
        "ctdt_id": ctdt_id,
        "cms": cms
    }
    return render(request, "sms/monhoc-ctdt.html", context)

@login_required
def ns_lop(request, ns_id):
    ls = Lop.objects.all()
    nls = NsLop.objects.filter(ns_id = ns_id).order_by('lop_id')
    if request.method == "POST":
        for l in ls:
            id = "C"+str(l.id)
            status = request.POST[id]
            print(id)
            print(status)
            nl = NsLop.objects.get(ns_id = ns_id, lop_id = l.id)
            nl.status=status
            nl.save() 
        #     id = "C"+str(stud.id)
        #     status = request.POST[id]
        #     dd = Diemdanh.objects.get(lichhoc_id = lh_id, sv_id=stud.id)
        #     dd.status=status
        #     dd.save() 
        # ttlh.status=1
        # ttlh.save()
        messages.success(request, "Cập nhật lớp thành công!")
        return redirect("ns_list")


    for l in ls:
        if not NsLop.objects.filter(ns_id = ns_id, lop_id = l.id).first():
            dd = NsLop(ns_id = ns_id, lop_id = l.id)
            dd.save()

    nls = NsLop.objects.filter(ns_id = ns_id).select_related("lop").order_by('lop_id')
    context = {
        "ns_id": ns_id,
        "nls": nls
    }
    return render(request, "sms/ns_lop.html", context)

@login_required
def single_ctdtmonhoc_old(request, ctdt_id):
        ctdtmonhoc1 = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, hocky = 1).select_related("monhoc")
        ctdtmonhoc2 = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, hocky = 2).select_related("monhoc")
        ctdtmonhoc3 = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, hocky = 3).select_related("monhoc")
        ctdtmonhoc4 = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, hocky = 4).select_related("monhoc")
        ten = Ctdt.objects.get(id = ctdt_id).ten
        context = {
            "ctdtmonhoc1": ctdtmonhoc1,
            "ctdtmonhoc2": ctdtmonhoc2,
            "ctdtmonhoc3": ctdtmonhoc3,
            "ctdtmonhoc4": ctdtmonhoc4,
            "ten": ten
        }
        return render(request, "sms/ctdt-monhoc_list.html", context)

@login_required
def single_ctdtmonhoc(request, ctdt_id):
        ctdt = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id).select_related("monhoc").order_by('hocky')
        ten = Ctdt.objects.get(id = ctdt_id).ten
        context = {
            "ctdt": ctdt,
            "ten": ten
        }
        return render(request, "sms/ctdt-monhoc_list.html", context)
@login_required
def lop_monhoc(request, lop_id):
        lm = LopMonhoc.objects.filter(lop_id = lop_id).select_related("lop", "monhoc")
        ten = Lop.objects.get(id = lop_id).ten
        context = {
            "lm": lm,
            "ten": ten,
            "lop_id": lop_id
        }
        return render(request, "sms/lop-monhoc_list.html", context)

@login_required
def hv_hp81_list(request, sv_id):
        hp81s = Hp81.objects.filter(sv_id = sv_id).select_related("sv", "hk")
        sv = Hssv.objects.get(id = sv_id)
        lop_id = sv.malop_id
        context = {
            "hp81s": hp81s,
            "ten": sv.hoten,
            "lop_id": lop_id,
            "sv_id": sv_id
        }
        return render(request, "sms/hv-hp81_list.html", context)

@login_required
def single_hs81lop(request, lop_id):
        ctdtmonhs811 = Hs81.objects.filter(lop_id = lop_id, hk = 1).select_related("sv", "lop")
        ctdtmonhs812 = Hs81.objects.filter(lop_id = lop_id, hk = 2).select_related("sv", "lop")
        ctdtmonhs813 = Hs81.objects.filter(lop_id = lop_id, hk = 3).select_related("sv", "lop")
        ctdtmonhs814 = Hs81.objects.filter(lop_id = lop_id, hk = 4).select_related("sv", "lop")
        ten = Lop.objects.get(id = lop_id).ten
        context = {
            "ctdtmonhoc1": ctdtmonhs811,
            "ctdtmonhoc2": ctdtmonhs812,
            "ctdtmonhoc3": ctdtmonhs813,
            "ctdtmonhoc4": ctdtmonhs814,
            "ten": ten
        }
        return render(request, "sms/lop-hs81_list.html", context)
   
def single_teacher(request, teacher_id):
    single_teacher = get_object_or_404(TeacherInfo, pk=teacher_id)
    context = {
        "single_teacher": single_teacher
    }
    return render(request, "sms/single_teacher.html", context)

@login_required
def create_lichhoc(request):
    if request.method == "POST":
        forms = CreateLichhoc(request.POST, request.FILES or None)
        lop = request.POST.get('lop', None)
        if forms.is_valid():
            forms.save()
        messages.success(request, "Lich hoc duoc tao thanh cong!")
        return redirect("lichhoclop_list", lop)
    else:
        forms = CreateLichhoc()
    context = {
        "forms": forms
    }
    return render(request, "sms/create_lichhoc.html", context)

@login_required
def create_hp81(request, sv_id):
    if request.method == "POST":
        hk_id = request.POST.get('hk', None)
        forms = CreateHp81(request.POST, request.FILES or None)
        if Hp81.objects.filter(hk_id = hk_id, sv_id=sv_id).first():
            #messages.success(request, "Mon hoc da ton taij!")
            messages.error(request, "Bản ghi đã tồn tại!")
        else:
            lop = request.POST.get('lop', None)
            if forms.is_valid():
                forms.save()
                messages.success(request, "Bản ghi duoc tao thanh cong!")
                return redirect("hv_hp81_list", sv_id)
    else:
        forms = CreateHp81()
    context = {
        "sv_id": sv_id,
        "forms": forms
    }
    return render(request, "sms/create_hp81.html", context)

@login_required
def create_lichhoclm(request, lopmh_id):
    if request.method == "POST":
        forms = CreateLichhoc(request.POST, request.FILES or None)
        lop = request.POST.get('lop', None)
        if forms.is_valid():
            forms.save()
        messages.success(request, "Lich hoc duoc tao thanh cong!")
        return redirect("lichhoclopmh_list", lopmh_id)
    else:
        forms = CreateLichhoc()

    lmh = LopMonhoc.objects.get(id = lopmh_id)
    forms = CreateLichhoc()
    context = {
        "forms": forms,
        "lop_id": lmh.lop_id,
        "monhoc_id": lmh.monhoc_id
    }
    return render(request, "sms/create_lichhoclm.html", context)

@login_required
def create_ctdtmonhoc(request):
    if request.method == "POST":
        forms = CreateCtdtMonhoc(request.POST, request.FILES or None)
        ctdt = request.POST.get('ctdt', None)
        if forms.is_valid():
            forms.save()
        messages.success(request, "Mon hoc duoc gan cho CTDT thanh cong!")
        return redirect("single_ctdtmonhoc", ctdt)
    else:
        forms = CreateCtdtMonhoc()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_ctdtmonhoc.html", context)

@login_required
#@permission_required('sms.add_lopmonhoc', raise_exception=True)
def create_lopmonhoc(request, lop_id):
    if not request.user.has_perm('sms.add_lopmonhoc'):
        return HttpResponseForbidden("Bạn không có quyền thực hiện thao tác thêm môn học!")
    if request.method == "POST":
        monhoc_id = request.POST.get('monhoc', None)
        if LopMonhoc.objects.filter(monhoc_id = monhoc_id, lop_id=lop_id).first():
            #messages.success(request, "Mon hoc da ton taij!")
            messages.error(request, "Môn học đã tồn tại!")
        else:
            forms = CreateLopMonhoc(request.POST, request.FILES or None)
            if forms.is_valid():
                forms.save()
                messages.success(request, "Môn học đã được thêm thành công!")
        #messages.success(request, "Mon hoc duoc them thanh cong!")
        return redirect("lop_monhoc", lop_id)
    forms = CreateLopMonhoc()

    query = '''select mh.id, mh.ma, mh.ten 
                            from sms_monhoc mh
                            inner join sms_ctdtmonhoc ctdtmh
								on mh.id = ctdtmh.monhoc_id and ctdtmh.status = 1
                            inner join sms_ctdt ctdt
								on ctdt.id = ctdtmh.ctdt_id
                            inner join sms_lop l
								on l.ctdt_id = ctdt.id
                            where l.id = %s and mh.id not in (select monhoc_id from sms_lopmonhoc where lop_id = %s)    
                            order by mh.id'''

    #sv = DiemdanhAll.objects.raw(query, [ttlh.lop_id, lh_id])
    #lmhs = LopMonhoc.objects.filter(lop_id = lop_id)
    mhs = Monhoc.objects.raw(query, [lop_id, lop_id])
    context = {
        "forms": forms,
        "mhs": mhs,
        "lop_id": lop_id
    }
    return render(request, "sms/create_lopmonhoc.html", context)

@login_required
def create_ctdt(request):
    if request.method == "POST":
        forms = CreateCtdt(request.POST, request.FILES or None)
        if Ctdt.objects.filter(ten = forms['ten'].value()).first():
            messages.error(request, "CTĐT đã tồn tại!")
            return redirect("ctdt_list")
        if forms.is_valid():
            forms.save()
            messages.success(request, "Tao moi CTDT thanh cong!")
            return redirect("ctdt_list")
    else:
        forms = CreateCtdt()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_ctdt.html", context)


@login_required
def create_lop(request):
    if request.method == "POST":
        forms = CreateLop(request.POST, request.FILES or None)
        if Lop.objects.filter(ma = forms['ma'].value()).first():
            messages.error(request, "Mã lớp đã tồn tại!")
            return redirect("lop_list")
        if forms.is_valid():
            lop = forms.save()
            hks= Hocky.objects.all()
            for hk in hks:
                lhk = LopHk.objects.create(hk_id = hk.id, lop_id = lop.id)
                lhk.save()        
            messages.success(request, "Tạo mới lớp thành công!")
        return redirect("lop_list")
    else:
        forms = CreateLop()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_lop.html", context)


@login_required
def create_sv(request):
    if request.method == "POST":
        forms = CreateSv(request.POST, request.FILES or None)
        #lh = request.POST.get('lichhoc', None)
        if Hssv.objects.filter(msv = forms['msv'].value()).first():
            messages.error(request, "Mã học viên đã tồn tại!")
        else:
            #return redirect("sv_list")
            if forms.is_valid():
                #uploaded_img = forms.save(commit=False)
                #uploaded_img.image_data = forms.cleaned_data['image'].file.read()
                #uploaded_img.save()
                forms.save()
                messages.success(request, "Tạo mới học viên thành công!")
                return redirect("svlop_list", forms.instance.malop_id)
    else:
        forms = CreateSv()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_sv.html", context)


@login_required
def create_gv(request):
    if request.method == "POST":
        forms = CreateGv(request.POST, request.FILES or None)
        if Hsgv.objects.filter(ma = forms['ma'].value()).first():
            messages.error(request, "Mã giáo viên đã tồn tại!")
            return redirect("gv_list")
        if forms.is_valid():
            forms.save()
        messages.success(request, "Tạo mới giáo viên thành công!")
        return redirect("gv_list")
    else:
        forms = CreateGv()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_gv.html", context)

@login_required
def create_ns(request):
    if request.method == "POST":
        forms = CreateNs(request.POST, request.FILES or None)
        if Hsns.objects.filter(ma = forms['ma'].value()).first():
            messages.error(request, "Mã nhân sự đã tồn tại!")
            return redirect("ns_list")
        if forms.is_valid():
            forms.save()
        messages.success(request, "Tạo mới nhân sự thành công!")
        return redirect("ns_list")
    else:
        forms = CreateNs()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_ns.html", context)

@login_required
def create_diemdanh(request, lh_id):
    print('hello')
    if request.method == "POST":
        forms = CreateDiemdanh(request.POST, request.FILES or None)
        #forms.initial['lichhoc']=7
        lh = request.POST.get('lichhoc', None)
        print('hello')
        if forms.is_valid():
            forms.save()
        messages.success(request, "Them sinh vien vang mat thanh cong!")
        return redirect("diemdanh_list", lh)
    else:
        forms = CreateDiemdanh()
    ttlh = Lichhoc.objects.all().select_related("lop", "monhoc").get(id = lh_id)
    #sv = Hssv.objects.all().filter(lop = ttlh.lop.ten)
    ds = Hssv.objects.all().filter(lop = ttlh.lop.ten)
    context = {
        "forms": forms,
        "lh_id": lh_id,
        "ttlh": ttlh,
        "dssv": ds
    }
    return render(request, "sms/create_diemdanh-new.html", context)

@login_required
def create_hocphi(request, lh_id):
    print('hello')
    if request.method == "POST":
        forms = CreateHocphi(request.POST, request.FILES or None)
        #forms.initial['lichhoc']=7
        lh = request.POST.get('lichhoc', None)
        #print('hello')
        if forms.is_valid():
            forms.save()
        messages.success(request, "Them thong tin hoc phi thanh cong!")
        return redirect("hocphi_list", lh_id)
    else:
        forms = CreateHocphi()
    ttlh = Lop.objects.get(id = lh_id)
    #sv = Hssv.objects.all().filter(lop = ttlh.lop.ten)
    ds = Hssv.objects.all().filter(lop = ttlh.ten)
    context = {
        "forms": forms,
        "lh_id": lh_id,
        "ttlh": ttlh,
        "dssv": ds
    }
    return render(request, "sms/create_hocphi.html", context)


@login_required
def create_diem(request, lh_id):
    print('hello')
    if request.method == "POST":
        forms = CreateDiem(request.POST, request.FILES or None)
        #forms.initial['lichhoc']=7
        #lh = request.POST.get('lichhoc', None)
        #print('hello')
        if forms.is_valid():
            forms.save()
        messages.success(request, "Them thong tin diem thanh cong!")
        return redirect("diem-lop_list", lh_id)
    else:
        forms = CreateDiem()
    ttlh = Lop.objects.get(id = lh_id)
    #sv = Hssv.objects.all().filter(lop = ttlh.lop.ten)
    ds = Hssv.objects.all().filter(lop = ttlh.ten)
    context = {
        "forms": forms,
        "lh_id": lh_id,
        "ttlh": ttlh,
        "dssv": ds
    }
    return render(request, "sms/create_diemtp.html", context)

@login_required
def create_diemdanh1(request):
    if request.method == "POST":
        forms = CreateDiemdanh(request.POST, request.FILES or None)
        lh = request.POST.get('lichhoc', None)
        if forms.is_valid():
            forms.save()
        messages.success(request, "Them sinh vien vang mat thanh cong!")
        return redirect("diemdanh_list", lh)
    else:
        forms = CreateDiemdanh()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_diemdanh.html", context)

def create_teacher(request):
    if request.method == "POST":
        forms = CreateTeacher(request.POST, request.FILES or None)

        if forms.is_valid():
            forms.save()
        messages.success(request, "Teacher Registration Successfully!")
        return redirect("teacher_list")
    else:
        forms = CreateTeacher()

    context = {
        "forms": forms
    }
    return render(request, "sms/create_teacher.html", context)

@login_required
def edit_lopmonhoc(request, lmh_id):
    lmh = LopMonhoc.objects.get(id=lmh_id)
    lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    lmh_forms = CreateLopMonhoc(instance=lmh)

    if request.method == "POST":
        edit_forms = CreateLopMonhoc(request.POST, request.FILES or None, instance=lmh)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit Mon hoc Info Successfully!")
            return redirect("lop_monhoc", lop_id)

    context = {
        "forms": lmh_forms,
        "lop_id": lop_id,
        "monhoc_id": monhoc_id
    }
    return render(request, "sms/edit_lopmonhoc.html", context)

@login_required
def edit_ttgv(request, lopmh_id, gv_id):

    if Ttgv.objects.filter(lopmh_id=lopmh_id, gv_id=gv_id).exists():
        ttgv = Ttgv.objects.get(lopmh_id=lopmh_id, gv_id=gv_id)
    else:
        ttgv = Ttgv(lopmh_id=lopmh_id, gv_id=gv_id)
        ttgv.save()

    ttgv_forms = CreateTtgv(instance=ttgv)

    if request.method == "POST":
        edit_forms = CreateTtgv(request.POST, request.FILES or None, instance=ttgv)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Cập nhật thông tin thanh toán thành công!")
            return redirect("gv-lmh-lst", lopmh_id)

    context = {
        "forms": ttgv_forms,
        "lopmh_id": lopmh_id,
        "gv_id": gv_id
    }
    return render(request, "sms/edit_ttgv.html", context)

@login_required
def history_lopmonhoc(request, lmh_id):

    lmh = LopMonhoc.objects.select_related("lop", "monhoc").get(id=lmh_id)
    
    #poll = Poll.objects.get(pk=poll_id)
    p = lmh.history.all()
    changes = []
    if p is not None and lmh_id:
        last = p.first()
        for all_changes in range(p.count()):
            new_record, old_record = last, last.prev_record
            if old_record is not None:
                delta = new_record.diff_against(old_record)
                changes.append(delta)
            last = old_record
            # create first time
            if all_changes == p.count()-1:
                delta = new_record.diff_against(new_record)
                changes.append(delta)

    context = {
        "lmh": lmh,
        "changes": changes
    }
    return render(request, "sms/history_lopmonhoc.html", context)

@login_required
def edit_lichhoc(request, lh_id):
    lh = Lichhoc.objects.get(id=lh_id)
    lmh_id = LopMonhoc.objects.get(lop_id=lh.lop_id, monhoc_id=lh.monhoc_id).id
    #lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    lh_forms = CreateLichhoc(instance=lh)

    if request.method == "POST":
        edit_forms = CreateLichhoc(request.POST, request.FILES or None, instance=lh)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit Mon hoc Info Successfully!")
            return redirect("lichhoclopmh_list", lmh_id)

    context = {
        "forms": lh_forms,
        "lop_id": lh.lop_id,
        "monhoc_id": lh.monhoc_id
#        "monhoc_id": monhoc_id
    }
    return render(request, "sms/edit_lichhoc.html", context)
@login_required
def edit_sv(request, sv_id):
    sv = Hssv.objects.get(id=sv_id)
    #lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    lh_forms = CreateSv(instance=sv)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if sv.image:
        mroot = os.path.join(base_dir, 'media',sv.image.name)
        troot = os.path.join(base_dir, 'static')
        #print(MEDIA_ROOT)
        #print(STATIC_ROOT)
        shutil.copy(mroot, troot + "\\uploads\\" + sv.image.name[8:]) # file will be renamed

    if request.method == "POST":
        edit_forms = CreateSv(request.POST, request.FILES or None, instance=sv)
        lop_id = request.POST.get('malop', None)
        #uploaded_file = UploadedFile.objects.get(pk=file_id)
        #response = HttpResponse(sv.image, content_type='application/force-download')
        #response['Content-Disposition'] = f'attachment; filename="{sv.image.name}"'
        #return response

        if edit_forms.is_valid():
            #uploaded_img = edit_forms.save(commit=False)
            #uploaded_img.image_data = edit_forms.cleaned_data['image'].file.read()
            edit_forms.save()
            messages.success(request, "Edit Học viên Info Successfully!")
            return redirect("svlop_list", lop_id)

    context = {
        "forms": lh_forms,
        "img": sv.image,
        "msv": sv.msv
    }
    return render(request, "sms/edit_sv.html", context)

@login_required
def details_sv(request, sv_id):
    sv = Hssv.objects.get(id=sv_id)
    lmh = LopMonhoc.objects.filter(lop_id = sv.malop_id).select_related("monhoc")
    dtp = Diemthanhphan.objects.filter(sv_id = sv_id)
    #ld = Loaidiem.objects.all()
    hks = Hocky.objects.all()
    hps = Hp81.objects.filter(sv_id = sv_id)

    for mh in lmh:
        ld = Loaidiem.objects.all()
        for l in ld:
            #hp.duno = hp.sotien2-hp.sotien1
            if Diemthanhphan.objects.filter(sv_id = sv_id,monhoc_id = mh.monhoc_id,tp_id = l.id).first():
                l.diem = Diemthanhphan.objects.filter(sv_id = sv_id,monhoc_id = mh.monhoc_id,tp_id = l.id)[0].diem
        mh.ttdiem = ld

    for hp in hps:
        hp.duno = hp.sotien2-hp.sotien1

    for hk in hks:
        if Hp81.objects.filter(sv_id = sv_id,hk_id = hk.id).first():
            hk.hp = Hp81.objects.filter(sv_id = sv_id,hk_id = hk.id)[0]
            hk.hp.duno = hk.hp.sotien2-hk.hp.sotien1
        else:
            hk.hp = None
    

    context = {
        "lmh": lmh,
        "ld": ld,
        "dtp": dtp,
        "hks": hks,
        "hps": hps,
        "msv": sv.msv,
        "ten": sv.hoten
    }
    return render(request, "sms/sv_details.html", context)

@login_required
def edit_hp81(request, hp81_id):
    hp = Hp81.objects.get(id=hp81_id)
    sv_id = hp.sv_id
    hk_id = hp.hk_id
    #lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    lh_forms = CreateHp81(instance=hp)

    if request.method == "POST":
        edit_forms = CreateHp81(request.POST, request.FILES or None, instance=hp)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit Info Successfully!")
            return redirect("hv_hp81_list", sv_id)

    context = {
        "forms": lh_forms,
        "sv_id": sv_id,
        "hk_id": hk_id
    }
    return render(request, "sms/edit_hp81.html", context)

@login_required
def edit_gv(request, gv_id):
    gv = Hsgv.objects.get(id=gv_id)
    #lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    lh_forms = CreateGv(instance=gv)

    if request.method == "POST":
        edit_forms = CreateGv(request.POST, request.FILES or None, instance=gv)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit Giao viên Info Successfully!")
            return redirect("gv_list")

    context = {
        "forms": lh_forms,
        "ma": gv.ma
    }
    return render(request, "sms/edit_gv.html", context)

@login_required
def edit_ns(request, ns_id):
    ns = Hsns.objects.get(id=ns_id)
    #lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    ns_forms = CreateNs(instance=ns)

    if request.method == "POST":
        edit_forms = CreateNs(request.POST, request.FILES or None, instance=ns)

        if edit_forms.is_valid():
            edit_forms.save()
            messages.success(request, "Edit nhân sự Info Successfully!")
            return redirect("ns_list")

    context = {
        "forms": ns_forms,
        "ma": ns.ma
    }
    return render(request, "sms/edit_ns.html", context)

@login_required
def edit_lop(request, lop_id):
    lop = Lop.objects.get(id=lop_id)
    #lop_id, monhoc_id = lmh.lop_id, lmh.monhoc_id
    lop_forms = CreateLop(instance=lop)
    lhk = LopHk.objects.select_related("hk").filter(lop_id=lop_id)

    if request.method == "POST":
        edit_forms = CreateLop(request.POST, request.FILES or None, instance=lop)

        if edit_forms.is_valid():
            edit_forms.save()
            for hk in lhk:
                start_hk = "start"+str(hk.hk.ma)
                end_hk = "end"+str(hk.hk.ma)
                elhk = LopHk.objects.get(lop_id = lop_id, hk_id = hk.hk.ma)
                elhk.start_hk = request.POST[start_hk] if request.POST[start_hk] else None
                elhk.end_hk = request.POST[end_hk] if request.POST[end_hk] else None

                elhk.save()
            messages.success(request, "Cập nhật thông tin lớp thành công!")
            return redirect("lop_list")

    context = {
        "forms": lop_forms,
        "ma": lop.ma,
        "lhk": lhk
    }
    return render(request, "sms/edit_lop.html", context)

def edit_teacher(request, pk):
    teacher_edit = TeacherInfo.objects.get(id=pk)
    edit_teacher_forms = CreateTeacher(instance=teacher_edit)

    if request.method == "POST":
        edit_teacher_forms = CreateTeacher(request.POST, request.FILES or None, instance=teacher_edit)

        if edit_teacher_forms.is_valid():
            edit_teacher_forms.save()
            messages.success(request, "Edit Teacher Info Successfully!")
            return redirect("teacher_list")

    context = {
        "edit_teacher_forms": edit_teacher_forms
    }
    return render(request, "sms/edit_teacher.html", context)

def delete_teacher(request, teacher_id):
    teacher_delete = TeacherInfo.objects.get(id=teacher_id)
    teacher_delete.delete()
    messages.success(request, "Delete Teacher Info Successfully")
    return redirect("teacher_list")

#@login_required
def react(request):

    return render(request, 'sms/product-index.html')

@login_required
def download_file1(request):
    path = "uploads/monhoc.xlsx"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = CreateUploadFile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "File mẫu được tải lên thành công!")
            return redirect('upload_file')
    else:
        form = CreateUploadFile()
    files = UploadedFile.objects.all()
    context = {
        'form': form,
        'files': files
    }
    return render(request, "sms/file_list.html", context)

@login_required
def download_file(request, file_id):
    uploaded_file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(uploaded_file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response

@login_required
def download_file2(request):
    import pandas as pd

    path = "uploads/pandas_simple.xlsx"
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Create a Pandas dataframe from the data.
    df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Create a chart object.
    chart = workbook.add_chart({"type": "column"})

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Configure the series of the chart from the dataframe data.
    chart.add_series({"values": ["Sheet1", 1, 1, max_row, 1]})

    # Insert the chart into the worksheet.
    worksheet.insert_chart(1, 3, chart)

    writer.close()    # Get the xlsxwriter objects from the dataframe writer object.

    #path = "uploads/monhoc.xlsx"
    #file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

    # Save the workbook to response object
    #workbook.save(response) # Chỉ dùng với openpyxl
#    writer.close()    # Get the xlsxwriter objects from the dataframe writer object.

    # Return the response object
 #   return response

@login_required
def report_hs81(request):
    hps = Hp81.objects.all().select_related("sv")
    if request.method == "POST":
            query_lop = request.POST.get('lop', None)
            query_tt = request.POST.get('trungtam', None)
            lh = Lop.objects.all().select_related("trungtam")
            if query_tt:
                lh = lh.filter(trungtam__ten__contains=query_tt)
            if query_lop:
                lh = lh.filter(lop__ten__contains=query_lop)     

            hps = hps.filter(sv__malop__in=lh.values_list('id', flat=True))
            messages.success(request, "Tìm kiếm thành công!")
    paginator = Paginator(hps, 50)
    page = request.GET.get('page')
    paged_students = paginator.get_page(page)
    context = {
        "hps": paged_students
    }
    return render(request, "sms/report_hs81.html", context)

@login_required()
def reset_pwd(request, ns_id):
    if not request.user.is_superuser:
        return redirect("/")
    ns = Hsns.objects.get(id = ns_id)
    # Check if username already exists
    if User.objects.filter(username=ns.ma).exists():
        user = User.objects.get(username=ns.ma)
        user.set_password(ns.ma + '@123654')
        user.save()    
        messages.success(request, "Reset password thành công!")
        return redirect('ns_list')    
    return redirect("ns_list")

@login_required()
def add_nsuser(request, id):
    if not request.user.is_superuser:
        return redirect("/")
    ns = Hsns.objects.get(id = id)
    # Check if username already exists
    if User.objects.filter(username=ns.ma).exists():
        messages.error(request, 'Username already exists')
        return redirect('ns_list')    
    
    user = User.objects.create_user(
        username=ns.ma,
        password=ns.ma + '@123654'
    )
    user.save()
    ns.user = user
    ns.save()
    messages.success(request, "Tạo tài khoản cho " + ns.hoten + " thành công")
    return redirect("ns_list")

@login_required
def user_changepwd(request):

    if request.method == "POST":
        user = User.objects.get(username = request.user.username)
        user.set_password(request.POST.get('password', None))
        user.save()    
        messages.success(request, "Thay doi password thanh cong!")
        return redirect("lop_list")
    return render(request, "sms/changepwd.html")