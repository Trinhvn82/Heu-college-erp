from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sms.models import Lop
from .models import Lop, Ctdt, Hssv, Hsgv, SvStatus, LopMonhoc, Hp81
from .models import Ctdt, Diemthanhphan, Hocky, HocphiStatus, Loaidiem, TeacherInfo, Hsgv, Hssv, CtdtMonhoc, Monhoc, Lop, Lichhoc, Hs81, Diemdanh, Diemthanhphan, Hocphi, LopMonhoc, DiemdanhAll
from .models import LopHk, Phong, Trungtam

# tickets/admin.py

@admin.action(description="Activate các môn học được chọn")
def activate_monhoc(modeladmin, request, queryset):
    queryset.update(status=1)


@admin.action(description="Deactivate các môn học được chọn")
def deactivate_monhoc(modeladmin, request, queryset):
    queryset.update(status=0)


class CtdtMonhocInline(admin.TabularInline):
    model = CtdtMonhoc
    fields = ["ctdt", "monhoc"]

    # optional: make the inline read-only
    readonly_fields = ["ctdt", "monhoc"]
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = True

class MonhocAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten", "chuongtrinh", "sotinchi"]
    search_fields = ["ma", "ten", "chuongtrinh"]
    inlines = [CtdtMonhocInline]
    #readonly_fields = ["tickets_left"]

class CtdtAdmin(admin.ModelAdmin):
    list_display = ["ten", "khoa", "khoahoc"]
    search_fields = ["ten", "khoa", "khoahoc"]
    inlines = [CtdtMonhocInline]
    #readonly_fields = ["tickets_left"]

class CtdtMonhocAdmin(admin.ModelAdmin):
    list_display = ["id","ctdt", "monhoc", "display_active"]
    search_fields = ["monhoc__ten", "ctdt__ten"]
    list_select_related = ["ctdt", "monhoc"]

    def display_active(self, obj):
        return obj.status == 1

    display_active.short_description = "Khả dụng"
    display_active.boolean = True
    display_active.admin_order_field = "status"
    actions = [activate_monhoc, deactivate_monhoc]


admin.site.register(Lop, SimpleHistoryAdmin)
admin.site.register(Ctdt, CtdtAdmin)
admin.site.register(Monhoc, MonhocAdmin)
admin.site.register(Hssv, SimpleHistoryAdmin)
admin.site.register(Hsgv, SimpleHistoryAdmin)
admin.site.register(LopMonhoc, SimpleHistoryAdmin)
admin.site.register(CtdtMonhoc, CtdtMonhocAdmin)
admin.site.register(Lichhoc, SimpleHistoryAdmin)
admin.site.register(Diemdanh, SimpleHistoryAdmin)
admin.site.register(Hs81, SimpleHistoryAdmin)
admin.site.register(Hp81, SimpleHistoryAdmin)
admin.site.register(Diemthanhphan, SimpleHistoryAdmin)
admin.site.register(LopHk, SimpleHistoryAdmin)
admin.site.register(Hocphi, SimpleHistoryAdmin)
admin.site.register(SvStatus, SimpleHistoryAdmin)
admin.site.register(Hocky, SimpleHistoryAdmin)
admin.site.register(HocphiStatus, SimpleHistoryAdmin)
admin.site.register(Loaidiem, SimpleHistoryAdmin)
admin.site.register(Phong, SimpleHistoryAdmin)
admin.site.register(Trungtam, SimpleHistoryAdmin)
#admin.site.register(Purchase)

class MonhocAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten", "chuongtrinh", "sotinchi"]
    #readonly_fields = ["tickets_left"]