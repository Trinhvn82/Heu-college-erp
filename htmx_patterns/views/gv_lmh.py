from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import partition
from htmx_patterns.models import Monster
from sms.models import GvLmh, LopMonhoc, Lop, Monhoc, Hsgv, CtdtMonhoc
from htmx_patterns.utils import for_htmx, is_htmx, make_get_request
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from guardian.shortcuts import assign_perm, remove_perm


@for_htmx(use_block_from_params=True)
@login_required
def view_gv_lmh(request: HttpRequest, gv_id):
    return _view_mh(request, gv_id)

@login_required
def view_gv_lmh_search(request,gv_id):
    #pass
    query = request.GET.get('search','')

    gv = Hsgv.objects.get(id = gv_id)
    lops = Lop.objects.filter(Q(ten__icontains=query))
    mhs = Monhoc.objects.filter(Q(ma__icontains=query) | Q(ten__icontains=query))
#    mhs = Monhoc.objects.filter(Q(ten__icontains=query))
    lmhs = LopMonhoc.objects.filter(lop__in=lops) | LopMonhoc.objects.filter(monhoc__in=mhs)
    sad_monsters = GvLmh.objects.filter(lopmh__in=lmhs,status=0, gv_id = gv_id).order_by('-status')
    happy_monsters = GvLmh.objects.filter(status = 1, gv_id = gv_id).order_by('-status')
    cms = happy_monsters | sad_monsters
    #return render(request, "sms/view_restart.html", {'sad_monsters':sad_monsters, 'happy_monsters':happy_monsters, "gv": gv})

    return render(request, "sms/gv_lopmh.html", {"gv": gv,'cms':cms})

def _view_mh(
    request: HttpRequest, gv_id
):

    gv = Hsgv.objects.get(id = gv_id)
    lmhs = LopMonhoc.objects.all()
    for lmh in lmhs:
        if not GvLmh.objects.filter(gv_id = gv_id, lopmh = lmh).exists():
            newlmh = GvLmh(gv_id = gv_id, lopmh = lmh)
            newlmh.save()
    gvlmhs = GvLmh.objects.filter(gv_id = gv_id).select_related('lopmh').order_by('-status')
    if request.method == "POST":
        list_of_ids = []

        for mh in gvlmhs:
            id = "C"+str(mh.id)
            status = request.POST.get(id, None)
            
            print(id)
            print(status)
            if status:
                list_of_ids.append(mh.id)

        gvlmhs.update(status = 0)
        gvlmhs.filter(id__in = list_of_ids).update(status=1)


        # assign role to gv based on lop mon hoc
        gmhs = GvLmh.objects.filter(gv = gv, status =1).select_related('lopmh')
        lmhs = LopMonhoc.objects.all()

        for lmh in lmhs:
            if gv.user.has_perm('assign_lopmonhoc', lmh):
                remove_perm('assign_lopmonhoc', gv.user, lmh)

        for lmh  in gmhs:
            assign_perm('assign_lopmonhoc', gv.user, lmh.lopmh)

        lop = Lop.objects.all()
        #Add Gv to assign_lop permission
        for l in lop:
            if gv.user.has_perm('assign_lop', l):
                remove_perm('assign_lop', gv.user, l)

        for l in lop:
            lmh = LopMonhoc.objects.filter(lop_id = l.id)
            if gmhs.filter(lopmh__in=lmh).exists():
                assign_perm('assign_lop', gv.user, l)


        #     id = "C"+str(stud.id)
        #     status = request.POST[id]
        #     dd = Diemdanh.objects.get(lichhoc_id = lh_id, sv_id=stud.id)
        #     dd.status=status
        #     dd.save() 
        # ttlh.status=1
        # ttlh.save()
        messages.success(request, "Cập nhật môn học thành công!")
        #return redirect("ctdt_list")

    context = {
        "gv": gv,
        "cms": gvlmhs
    }
    return TemplateResponse(
        request,
        "sms/gv_lopmh.html",
        context
    )
