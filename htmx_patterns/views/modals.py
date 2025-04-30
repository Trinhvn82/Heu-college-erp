import json

from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from sms.models import LopMonhoc

from ..models import Monster
from ..utils import for_htmx


@for_htmx(use_block_from_params=True)
def main(request: HttpRequest):
    return TemplateResponse(
        request,
        "modals_main.html",
        {
            "monsters": Monster.objects.all().order_by("name"),
        },
    )


class CreateMonsterForm(ModelForm):
    class Meta:
        model = Monster
        fields = ["name", "is_happy"]


@for_htmx(use_block_from_params=True)
def create_monster(request: HttpRequest):
    print("create_monster")
    if request.method == "POST":
        form = CreateMonsterForm(request.POST)
        if form.is_valid():
            monster = form.save()
            return HttpResponse(
                headers={
                    "Hx-Trigger": json.dumps(
                        {
                            "closeModal": True,
                            "monsterCreated": monster.id,
                        }
                    )
                }
            )
    else:
        form = CreateMonsterForm()
    return TemplateResponse(request, "sms/modals_create_monster.html", {"form": form})

@for_htmx(use_block_from_params=True)
def show_history(request: HttpRequest, lmh_id):
    print("create_monster")
    print(lmh_id)
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
        "changes": changes
    }
    return TemplateResponse(request, "sms/modals_create_monster.html", context)
