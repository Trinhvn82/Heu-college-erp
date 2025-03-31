from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import partition
from htmx_patterns.models import Monster
from sms.models import GvLmh, LopMonhoc, Lop, Monhoc, Hsgv
from htmx_patterns.utils import for_htmx, is_htmx, make_get_request
from django.db.models import Q
from django.shortcuts import render


@for_htmx(use_block_from_params=True)
def view_restart(request: HttpRequest, gv_id):
    return _view_restart(request, gv_id)

def view_search(request, gv_id):
    query = request.GET.get('search','')
    #sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)
    print('searching: ' + query)
    gv = Hsgv.objects.get(id = gv_id)
    lops = Lop.objects.filter(Q(ten__icontains=query))
    mhs = Monhoc.objects.filter(Q(ma__icontains=query) | Q(ten__icontains=query))
    lmhs = LopMonhoc.objects.filter(lop__in=lops) | LopMonhoc.objects.filter(monhoc__in=mhs)
    sad_monsters = GvLmh.objects.filter(lopmh__in=lmhs,status=0, gv_id = gv_id)
    happy_monsters = GvLmh.objects.filter(status = 1, gv_id = gv_id)
    return render(request, "sms/view_restart.html", {'sad_monsters':sad_monsters, 'happy_monsters':happy_monsters, "gv": gv})

def _view_restart(
    request: HttpRequest, gv_id,
    *,
    selected_happy_monsters: list[Monster] | None = None,
    selected_sad_monsters: list[Monster] | None = None,
):
    #check if not existe, create neew record
    gv = Hsgv.objects.get(id = gv_id)
    lmhs = LopMonhoc.objects.all()
    for lmh in lmhs:
        if not GvLmh.objects.filter(gv_id = gv_id, lopmh = lmh).exists():
            newlmh = GvLmh(gv_id = gv_id, lopmh = lmh)
            newlmh.save()

    monsters = GvLmh.objects.filter(gv_id = gv_id).select_related('lopmh')
    sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)

    if request.method == "POST":
        selected_happy_monsters = [
            monster for monster in happy_monsters if f"happy_monster_{monster.id}" in request.POST
        ]
        # id = request.POST.get('sad_monsters', None)
        # print(type(id))
        # if id:
        #     selected_sad_monsters = [monster for monster in sad_monsters if monster.id==int(id)]
        selected_sad_monsters = [monster for monster in sad_monsters if f"sad_monster_{monster.id}" in request.POST]
        if "kick" in request.POST:
            for monster in selected_happy_monsters:
                monster.kick()
            selected_happy_monsters = []
        if "hug" in request.POST:
            for monster in selected_sad_monsters:
                monster.hug()
            selected_sad_monsters = []
        if is_htmx(request):
            return _view_restart(
                make_get_request(request), 
                gv.id,
                selected_sad_monsters=selected_sad_monsters,
                selected_happy_monsters=selected_happy_monsters,
            )
        return HttpResponseRedirect("")

    return TemplateResponse(
        request,
        "sms/view_restart.html",
        {
            "happy_monsters": happy_monsters,
            "sad_monsters": sad_monsters,
            "gv": gv,
            "selected_happy_monsters": selected_happy_monsters or [],
            "selected_sad_monsters": selected_sad_monsters or [],
        },
    )
