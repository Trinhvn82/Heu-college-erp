from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import partition
from htmx_patterns.models import Monster
from sms.models import GvLmh, LopMonhoc, Lop, Monhoc, Hsgv
from htmx_patterns.utils import for_htmx, is_htmx, make_get_request
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


@for_htmx(use_block_from_params=True)
@login_required
def view_tb(request: HttpRequest):
    return _view_tb(request)

@login_required
def view_tb_search(request):
    #pass
    query = request.GET.get('search','')
    #sad_monsters, happy_monsters = partition(lambda m: m.status, monsters)
    print('searching: ' + query)
    #sad_monsters = request.user.notifications.filter(Q(actor__username__icontains=query) | Q(verb__icontains=query) | Q(level__icontains=query))
    sad_monsters = request.user.notifications.filter(Q(verb__icontains=query) | Q(level__icontains=query))[0:50]

    return render(request, "sms/tb_list_htmx.html", {'sad_monsters':sad_monsters})

def _view_tb(
    request: HttpRequest,
    *,
    selected_happy_monsters: list[Monster] | None = None,
    selected_sad_monsters: list[Monster] | None = None,
):

    tbaos = request.user.notifications.all()[0:50]
    sad_monsters, happy_monsters = tbaos,tbaos

    return TemplateResponse(
        request,
        "sms/tb_list_htmx.html",
        {
            "happy_monsters": happy_monsters,
            "sad_monsters": sad_monsters,
            "selected_happy_monsters": selected_happy_monsters or [],
            "selected_sad_monsters": selected_sad_monsters or [],
        },
    )
