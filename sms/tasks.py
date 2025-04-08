from django.shortcuts import render, get_object_or_404, redirect
from notifications.signals import notify
from django_q.models import Schedule
from django.contrib.auth import get_user_model
from .models import Lop, LopHk, Hs81, Hp81, NsLop, LopMonhoc, Ttgv, Hsgv, Lichhoc, Hssv
import datetime
from django.db.models import Sum
#from django.contrib.auth.models import User


User = get_user_model()

def fetch_tbs_new():

#    print("fetch_tbs is running...")

    user = User.objects.get(username='System')
    #('success', 'info', 'warning', 'error') (default=info)

   #TB về thông tin học kỳ
    lops = Lop.objects.all()
    for lop in lops:
        hks = LopHk.objects.filter(lop_id = lop.id).select_related('hk')
        svs = Hssv.objects.filter(lop_id = lop.id)
        for hk in hks:
            if hk.start_hk == None or hk.end_hk == None:
                nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                for nsl in nsls:
                    if nsl.ns.user:
                        print("fetch_tbs is running...")
                        notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' thiếu thông tin học kỳ '+ str(hk.hk.ma), level='warning')
                        #('success', 'info', 'warning', 'error') (default=info)
            if hk.end_hk:
                delta = datetime.date.today()-hk.end_hk
                # Check if còn thiếu hs, hp khi đã kết thúc học kỳ 2 tháng
                if delta.days > 60:
                    for sv in svs:
                        if not Hs81.objects.filter(sv = sv, hk = hk.hk).exists():
                            nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                            for nsl in nsls:
                                if nsl.ns.user:
                                    print("fetch_tbs is running...")
                                    notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' học kỳ '+ str(hk.hk.ma) + ' học viên ' + sv.hoten + ' thiếu thông tin HS81', level='warning')
                                    #('success', 'info', 'warning', 'error') (default=info)
                    if Hs81.objects.filter(sv__in = svs, hk = hk.hk, status="Thiếu").exists():
                        for hs in Hs81.objects.filter(sv__in = svs, hk = hk.hk, status="Thiếu").select_related('sv'):
                            nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                            for nsl in nsls:
                                if nsl.ns.user:
                                    print("fetch_tbs is running...")
                                    notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' học kỳ '+ str(hk.hk.ma) + ' học viên ' + hs.sv.hoten + ' thiếu HS81', level='warning')
                                    #('success', 'info', 'warning', 'error') (default=info)

                    for sv in svs:
                        if not Hp81.objects.filter(sv = sv, hk = hk.hk).exists():
                            nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                            for nsl in nsls:
                                if nsl.ns.user:
                                    print("fetch_tbs is running...")
                                    notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' học kỳ '+ str(hk.hk.ma) + ' học viên ' + sv.hoten + ' thiếu thông tin HP81', level='warning')
                                    #('success', 'info', 'warning', 'error') (default=info)
                    if Hp81.objects.filter(sv__in = svs, hk = hk.hk, status=1).exists():
                        for hs in Hp81.objects.filter(sv__in = svs, hk = hk.hk, status=3).select_related('sv'):
                            nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                            for nsl in nsls:
                                if nsl.ns.user:
                                    print("fetch_tbs is running...")
                                    notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' học kỳ '+ str(hk.hk.ma) + ' học viên ' + hs.sv.hoten + ' chưa nộp tiền cho HEU', level='warning')
                                    #('success', 'info', 'warning', 'error') (default=info)
                # Check if môn học chưa kết thúc khi đã kết thúc học kỳ 1 tuần
                if delta.days > 7:
                    if LopMonhoc.objects.filter(lop_id = lop.id, hk = hk.hk ,status="Lập kế hoạch").exists():
                        for hs in LopMonhoc.objects.filter(lop_id = lop.id, hk = hk.hk, status="Lập kế hoạch").select_related('monhoc'):
                            nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                            for nsl in nsls:
                                if nsl.ns.user:
                                    print("fetch_tbs is running...")
                                    notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' học kỳ '+ str(hk.hk.ma) + ' có môn học ' + hs.monhoc.ten + ' chưa hoàn thành', level='warning')
                                    #('success', 'info', 'warning', 'error') (default=info)
                # Check if chưa thanh toán cho gv khi đã kết thúc học kỳ 1 tháng
                if delta.days > 30:

                    lmhs = LopMonhoc.objects.filter(lop = lop, hk = hk.hk, status="Đã hoàn thành").select_related("monhoc", "lop")

                    
                    for lmh in lmhs:
                        lhs = Lichhoc.objects.filter(lmh = lmh).select_related("lop", "monhoc")
                        gvs = Hsgv.objects.filter(id__in = lhs.values_list('giaovien_id', flat=True))
                        for gv in gvs:

                            lhs = Lichhoc.objects.filter(lmh = lmh, giaovien = gv)
                            if not Ttgv.objects.filter(lopmh = lmh, gv = gv).exists():

                                nsls = NsLop.objects.filter(lop_id = lop.id, status=1).select_related('ns')
                                for nsl in nsls:
                                    if nsl.ns.user:
                                        print("fetch_tbs is running...")
                                        notify.send(sender=user, recipient=nsl.ns.user, verb='Lớp:' + lop.ten + ' học kỳ '+ str(hk.hk.ma) + ' có môn học ' + lmh.monhoc.ten + ' chưa thanh toán cho giáo viên ' + gv.ma + '|' + gv.hoten, level='warning')
                                        #('success', 'info', 'warning', 'error') (default=info)
def create_tbs(request):
    # This function is called by the schedule to fetch tbs
    # You can add any logic here that you want to run periodically
    # For example, you can send notifications to users or perform some database operations
    fetch_tbs_new()
    return redirect('tb_list')  # Redirect to the desired URL after fetching tbs