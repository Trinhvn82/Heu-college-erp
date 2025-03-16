from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sms.models import Lop
from .models import Lop, Ctdt, Hssv, Hsgv, SvStatus, LopMonhoc, Hp81
from .models import Ctdt, Diemthanhphan, Hocky, HocphiStatus, Loaidiem, TeacherInfo, Hsgv, Hssv, CtdtMonhoc, Monhoc, Lop, Lichhoc, Hs81, Diemdanh, Diemthanhphan, Hocphi, LopMonhoc, DiemdanhAll
from .models import LopHk, Phong, Trungtam, LogDiem, NsLop, NsPhong,HeDT,Khoahoc,Nganh

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
    readonly_fields = ["id","ctdt", "monhoc"]
    can_delete = True
    max_num = 0
    extra = 0
    show_change_link = True

class LopHKInline(admin.TabularInline):
    model = LopHk
    fields = ["hk", "start_hk", "end_hk"]

    # optional: make the inline read-only
    readonly_fields = ["hk", "start_hk", "end_hk"]
    can_delete = True
    max_num = 0
    extra = 0
    show_change_link = True

class SvInline(admin.TabularInline):
    model = Hssv
    fields = ["msv", "hoten", "namsinh", "gioitinh", "cccd", "sdths", "status"]

    # optional: make the inline read-only
    readonly_fields = ["msv", "hoten", "namsinh", "gioitinh", "cccd", "sdths", "status"]
    can_delete = False
    max_num = 0
    extra = 0
    show_change_link = False

class LopMonhocInline(admin.TabularInline):
    model = LopMonhoc
    fields = ["monhoc", "ngaystart", "ngayend", "status"]

    # optional: make the inline read-only
    readonly_fields = ["monhoc", "ngaystart", "ngayend", "status"]
    can_delete = True
    max_num = 0
    extra = 0
    show_change_link = True

class MonhocAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten", "chuongtrinh", "sotinchi"]
    search_fields = ["ma", "ten", "chuongtrinh"]
    inlines = [CtdtMonhocInline]
    #readonly_fields = ["tickets_left"]

class LopHKAdmin(admin.ModelAdmin):
    list_display = ["lop","hk", "start_hk", "end_hk"]
    search_fields = ["lop"]


class CtdtAdmin(admin.ModelAdmin):
    list_display = ["ten", "khoa", "khoahoc"]
    search_fields = ["ten", "khoa", "khoahoc"]
    inlines = [CtdtMonhocInline]
    #readonly_fields = ["tickets_left"]

class CtdtMonhocAdmin(admin.ModelAdmin):
    list_display = ["id","ctdt", "monhoc", "display_active"]
    search_fields = ["monhoc__ten", "ctdt__ten"]
    list_select_related = ["ctdt", "monhoc"]
    
    list_filter = ["monhoc__ten", "ctdt__ten"]  
    
    def display_active(self, obj):
        return obj.status == 1

    display_active.short_description = "Có hiệu lực"
    display_active.boolean = True

    actions = [activate_monhoc, deactivate_monhoc]

    
class LopAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten", "trungtam", "ctdt"]
    search_fields = ["ma", "ten", "trungtam__ten", "ctdt__ten"]
    list_select_related = ["ctdt", "trungtam"]
    inlines = [LopHKInline,LopMonhocInline, SvInline]
    #inlines = [SvInline]

class DanhmucAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten"]
    search_fields = ["ma", "ten"]

class LoaiDiemAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten", "heso","trunglap"]
    search_fields = ["ma", "ten"]

class DiemTPAdmin(admin.ModelAdmin):
    list_display = ["sv","monhoc", "tp", "diem", "log"]
    search_fields = ["monhoc__ten"]
    list_filter = ["tp__ten", "log__id"]

class LopMonhocAdmin(admin.ModelAdmin):
    list_display = ["lop","monhoc", "ngaystart", "ngayend", "status"]
    search_fields = ["monhoc__ten", "lop__ten"]
    list_select_related = ["lop", "monhoc"]

class NsLopAdmin(admin.ModelAdmin):
    list_display = ["ns","lop"]
    search_fields = ["ns__ten", "lop__ten"]
    list_select_related = ["lop", "ns"]

class NsPhongAdmin(admin.ModelAdmin):
    list_display = ["ns","phong"]
    search_fields = ["ns__ten", "phong__ten"]
    list_select_related = ["phong", "ns"]


admin.site.register(Lop, LopAdmin)
admin.site.register(NsLop, NsLopAdmin)
admin.site.register(NsPhong, NsPhongAdmin)
admin.site.register(Ctdt, CtdtAdmin)
admin.site.register(Monhoc, MonhocAdmin)
admin.site.register(Hssv, SimpleHistoryAdmin)
admin.site.register(Hsgv, SimpleHistoryAdmin)
admin.site.register(LopMonhoc, LopMonhocAdmin)
admin.site.register(CtdtMonhoc, CtdtMonhocAdmin)
admin.site.register(Lichhoc, SimpleHistoryAdmin)
admin.site.register(Diemdanh, SimpleHistoryAdmin)
admin.site.register(Hs81, SimpleHistoryAdmin)
admin.site.register(Hp81, SimpleHistoryAdmin)
admin.site.register(Diemthanhphan, DiemTPAdmin)
admin.site.register(LopHk, LopHKAdmin)
#admin.site.register(Hocphi, SimpleHistoryAdmin)
admin.site.register(Loaidiem, LoaiDiemAdmin)

admin.site.register(Hocky, DanhmucAdmin)
admin.site.register(HocphiStatus, DanhmucAdmin)
admin.site.register(SvStatus, DanhmucAdmin)
admin.site.register(Phong, DanhmucAdmin)

admin.site.register(HeDT, DanhmucAdmin)
admin.site.register(Trungtam, DanhmucAdmin)
admin.site.register(Khoahoc, DanhmucAdmin)
admin.site.register(Nganh, DanhmucAdmin)

admin.site.register(LogDiem, SimpleHistoryAdmin)

#admin.site.register(Purchase)

class MonhocAdmin(admin.ModelAdmin):
    list_display = ["ma", "ten", "chuongtrinh", "sotinchi"]
    #readonly_fields = ["tickets_left"]