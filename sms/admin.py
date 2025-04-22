from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from sms.models import Lop
from .models import Lop, Ctdt, Hssv, Hsgv, Hsns, SvStatus, LopMonhoc, Hp81
from .models import Ctdt, Diemthanhphan, Hocky, HocphiStatus, Loaidiem, TeacherInfo, Hsgv, Hssv, CtdtMonhoc, Monhoc, Lop, Lichhoc, Hs81, Diemdanh, Diemthanhphan, Hocphi, LopMonhoc, DiemdanhAll
from .models import LopHk, Phong, Trungtam, LogDiem, NsLop, NsPhong,HeDT,Khoahoc,Nganh, Ttgv, GvLop, GvLmh

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

class NonDeleteModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None): # note the obj=None
        return True

class NonDeleteAndAddModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None): # note the obj=None
        return True
    def has_add_permission(self, request, obj=None): # note the obj=None
        return True

class MonhocAdmin(NonDeleteModelAdmin):
    list_display = ["ma", "ten", "chuongtrinh", "sotinchi"]
    search_fields = ["ma", "ten", "chuongtrinh"]
    inlines = [CtdtMonhocInline]
    #readonly_fields = ["tickets_left"]

class GvLmhAdmin(NonDeleteModelAdmin):
    list_display = ["gv", "lopmh"]
    search_fields = ["gv__hoten"]
    #readonly_fields = ["tickets_left"]

class LopHKAdmin(NonDeleteModelAdmin):
    list_display = ["lop","hk", "start_hk", "end_hk"]
    search_fields = ["lop__ten"]

#class CtdtAdmin(admin.ModelAdmin):
class CtdtAdmin(NonDeleteModelAdmin):
    list_display = ["ten", "khoa", "khoahoc"]
    search_fields = ["ten", "khoa", "khoahoc"]
    inlines = [CtdtMonhocInline]
    #readonly_fields = ["tickets_left"]

class CtdtMonhocAdmin(NonDeleteModelAdmin):
    list_display = ["id","ctdt", "monhoc", "display_active"]
    search_fields = ["monhoc__ten", "ctdt__ten"]
    list_select_related = ["ctdt", "monhoc"]
    
    list_filter = ["monhoc__ten", "ctdt__ten"]  
    
    def display_active(self, obj):
        return obj.status == 1

    display_active.short_description = "Có hiệu lực"
    display_active.boolean = True

    actions = [activate_monhoc, deactivate_monhoc]

    
class LopAdmin(NonDeleteAndAddModelAdmin):
    list_display = ["ma", "ten", "trungtam", "ctdt"]
    search_fields = ["ma", "ten", "trungtam__ten", "ctdt__ten"]
    list_select_related = ["ctdt", "trungtam"]
    inlines = [LopHKInline,LopMonhocInline, SvInline]
    #inlines = [SvInline]

class HssvAdmin(NonDeleteAndAddModelAdmin):
    list_display = ["msv", "hoten"]
    search_fields = ["hoten"]

class HsgvAdmin(NonDeleteAndAddModelAdmin):
    list_display = ["ma", "hoten"]
    search_fields = ["hoten"]

class HsnsAdmin(NonDeleteAndAddModelAdmin):
    list_display = ["ma", "hoten"]
    search_fields = ["hoten"]

class DanhmucAdmin(NonDeleteModelAdmin):
    list_display = ["ma", "ten"]
    search_fields = ["ma", "ten"]

class LoaiDiemAdmin(NonDeleteModelAdmin):
    list_display = ["ma", "ten", "heso","trunglap"]
    search_fields = ["ma", "ten"]

class DiemTPAdmin(NonDeleteModelAdmin):
    list_display = ["sv","monhoc", "tp", "diem", "log"]
    search_fields = ["monhoc__ten"]
    list_filter = ["tp__ten", "log__id"]

class LopMonhocAdmin(NonDeleteAndAddModelAdmin):
    list_display = ["lop","monhoc", "ngaystart", "ngayend", "status"]
    search_fields = ["monhoc__ten", "lop__ten"]
    list_select_related = ["lop", "monhoc"]

class NsLopAdmin(NonDeleteModelAdmin):
    list_display = ["ns","lop"]
    search_fields = ["ns__ten", "lop__ten"]
    list_select_related = ["lop", "ns"]

class GvLopAdmin(NonDeleteModelAdmin):
    list_display = ["gv","lop"]
    search_fields = ["gv__hoten"]
    list_select_related = ["lop", "gv"]

class NsPhongAdmin(NonDeleteModelAdmin):
    list_display = ["ns","phong"]
    search_fields = ["ns__ten", "phong__ten"]
    list_select_related = ["phong", "ns"]


admin.site.register(Lop, LopAdmin)
admin.site.register(NsLop, NsLopAdmin)
admin.site.register(NsPhong, NsPhongAdmin)
admin.site.register(GvLop, GvLopAdmin)
admin.site.register(Ctdt, CtdtAdmin)
admin.site.register(Hssv, HssvAdmin)
admin.site.register(Hsgv, HsgvAdmin)
admin.site.register(Hsns, HsnsAdmin)
admin.site.register(LopMonhoc, LopMonhocAdmin)
admin.site.register(CtdtMonhoc, CtdtMonhocAdmin)
admin.site.register(Lichhoc, NonDeleteModelAdmin)
admin.site.register(Diemdanh, NonDeleteModelAdmin)
admin.site.register(Hs81, NonDeleteModelAdmin)
admin.site.register(Hp81, NonDeleteModelAdmin)
admin.site.register(Diemthanhphan, DiemTPAdmin)
admin.site.register(LopHk, LopHKAdmin)
admin.site.register(Hocphi, SimpleHistoryAdmin)
admin.site.register(Ttgv, GvLmhAdmin)
admin.site.register(GvLmh, GvLmhAdmin)
admin.site.register(LogDiem, NonDeleteModelAdmin)

# Danh mục sections
admin.site.register(Loaidiem, LoaiDiemAdmin)
admin.site.register(Monhoc, MonhocAdmin)
admin.site.register(Hocky, DanhmucAdmin)
admin.site.register(HocphiStatus, DanhmucAdmin)
admin.site.register(SvStatus, DanhmucAdmin)
admin.site.register(Phong, DanhmucAdmin)
admin.site.register(HeDT, DanhmucAdmin)
admin.site.register(Trungtam, DanhmucAdmin)
admin.site.register(Khoahoc, DanhmucAdmin)
admin.site.register(Nganh, DanhmucAdmin)




