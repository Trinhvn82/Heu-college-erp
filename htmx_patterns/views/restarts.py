from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import partition
from htmx_patterns.models import Monster
from sms.models import GvLmh, LopMonhoc, Lop, Monhoc
from htmx_patterns.utils import for_htmx, is_htmx, make_get_request
from django.db.models import Q
from django.shortcuts import render


@for_htmx(use_block_from_params=True)
def view_restart(request: HttpRequest, gv_id):
    return _view_restart(request)

def view_search(request):
    query = request.GET.get('search','')
    #sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)
    print('searching: ' + query)
    lops = Lop.objects.filter(Q(ten__icontains=query))
    mhs = Monhoc.objects.filter(Q(ma__icontains=query) | Q(ten__icontains=query))
    lmhs = LopMonhoc.objects.filter(lop__in=lops) | LopMonhoc.objects.filter(monhoc__in=mhs)
    sad_monsters = GvLmh.objects.filter(lopmh__in=lmhs,status=0)
    happy_monsters = GvLmh.objects.filter(status = 1)
    return render(request, "sms/view_restart.html", {'sad_monsters':sad_monsters, 'happy_monsters':happy_monsters})

def _view_restart(
    request: HttpRequest,
    *,
    selected_happy_monsters: list[Monster] | None = None,
    selected_sad_monsters: list[Monster] | None = None,
):
    monsters = GvLmh.objects.all().select_related('lopmh')
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
            "selected_happy_monsters": selected_happy_monsters or [],
            "selected_sad_monsters": selected_sad_monsters or [],
        },
    )
