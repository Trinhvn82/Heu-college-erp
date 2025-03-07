from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from sms.models import Lop
from .models import Lop, Ctdt, Hssv, Hsgv, SvStatus, LopMonhoc, Hp81
from .models import Ctdt, Diemthanhphan, Hocky, HocphiStatus, Loaidiem, TeacherInfo, Hsgv, Hssv, CtdtMonhoc, Monhoc, Lop, Lichhoc, Hs81, Diemdanh, Diemthanhphan, Hocphi, LopMonhoc, DiemdanhAll
from .models import LopHk, Phong, Trungtam

admin.site.register(Lop, SimpleHistoryAdmin)
admin.site.register(Ctdt, SimpleHistoryAdmin)
admin.site.register(Monhoc, SimpleHistoryAdmin)
admin.site.register(Hssv, SimpleHistoryAdmin)
admin.site.register(Hsgv, SimpleHistoryAdmin)
admin.site.register(LopMonhoc, SimpleHistoryAdmin)
admin.site.register(CtdtMonhoc, SimpleHistoryAdmin)
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
