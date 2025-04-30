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


@for_htmx(use_block_from_params=True)
@login_required
def view_mh(request: HttpRequest, ctdt_id):
    return _view_mh(request, ctdt_id)

@login_required
def view_mh_search(request,ctdt_id):
    #pass
    query = request.GET.get('search','')
    #sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)
    print('searching: ' + query)
    #sad_monsters = request.user.notifications.filter(Q(actor__username__icontains=query) | Q(verb__icontains=query) | Q(level__icontains=query))
    mhs = Monhoc.objects.filter(Q(ma__icontains=query) | Q(ten__icontains=query) | Q(chuongtrinh__icontains=query))
    cms1 = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, status = 1).select_related("monhoc").order_by('-status','monhoc_id')
    cms0 = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, status =0, monhoc__in = mhs).select_related("monhoc").order_by('-status','monhoc_id')
    cms = cms1 | cms0
    return render(request, "sms/monhoc-ctdt-htmx.html", {"ctdt_id": ctdt_id,'cms':cms})

def _view_mh(
    request: HttpRequest, ctdt_id
):

    mhs = Monhoc.objects.all()
    cms = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id).order_by('monhoc_id')
    if request.method == "POST":
        list_of_ids = []

        for mh in cms:
            id = "C"+str(mh.id)
            status = request.POST.get(id, None)
            
            print(id)
            print(status)
            if status:
                list_of_ids.append(mh.id)

        cms.update(status = 0)
        cms.filter(id__in = list_of_ids).update(status=1)
        #     id = "C"+str(stud.id)
        #     status = request.POST[id]
        #     dd = Diemdanh.objects.get(lichhoc_id = lh_id, sv_id=stud.id)
        #     dd.status=status
        #     dd.save() 
        # ttlh.status=1
        # ttlh.save()
        messages.success(request, "Cập nhật môn học thành công!")
        #return redirect("ctdt_list")


    for mh in mhs:
        if not CtdtMonhoc.objects.filter(ctdt_id = ctdt_id, monhoc_id = mh.id).first():
            dd = CtdtMonhoc(ctdt_id = ctdt_id, monhoc_id = mh.id)
            dd.save()

    cms = CtdtMonhoc.objects.filter(ctdt_id = ctdt_id).select_related("monhoc").order_by('-status','monhoc_id')
    context = {
        "ctdt_id": ctdt_id,
        "cms": cms
    }
    return TemplateResponse(
        request,
        "sms/monhoc-ctdt-htmx.html",
        context
    )
