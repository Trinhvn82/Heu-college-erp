from django.urls import path, include
from . import views, views_report
from django.contrib import admin
from info.views import add_hvuser, add_nsuser, reset_pwd, user_changepwd, ns_quyen,add_gvuser, reset_pwd_gv,reset_pwd_hv
from htmx_patterns.views.restarts import view_restart, view_search
from htmx_patterns.views.thongbao import view_tb, view_tb_search 
from htmx_patterns.views.notifications import live_tester, make_notification
from sms.tasks import create_tbs

urlpatterns = [
    path('', views.index, name='index'),
    #path('alllop/', views.lop_list, name='lop_list'),
    #path('', views.index, name='t_clas'),
    path('teacher/<slug:teacher_id>/<int:choice>/Classes/',
         views.t_clas, name='t_clas'),
    path('teacher/<slug:teacher_id>/t_timetable/',
         views.t_timetable, name='t_timetable'),
    path('allteachers/', views.teacher_list, name='teacher_list'),
    path('allsv/', views.sv_list, name='sv_list'),
    path('allgv/', views.gv_list, name='gv_list'),
    path('allns/', views.ns_list, name='ns_list'),

    path('ns_lop/<int:ns_id>/', views.ns_lop, name='ns_lop'),
    path('ns_quyen/<int:ns_id>/', ns_quyen, name='ns_quyen'),

    path('gv_lop/<int:gv_id>/', views.gv_lop, name='gv_lop'),
    path('gv_monhoc/<int:gv_id>/', views.gv_monhoc, name='gv_monhoc'),
    path('gv_lmh/<int:gv_id>/', views.gv_lmh, name='gv_lmh'),

    path('gv_lmh_htmx/<int:gv_id>/', view_restart, name='gv_lmh_htmx'),
    path('search_lmh_htmx/<int:gv_id>/', view_search, name='search_lmh_htmx'),

    path('tb_htmx/', view_tb, name='tb_list_htmx'),
    path('search_tb_htmx/', view_tb_search, name='search_tb_htmx'),

    path('notifications/', live_tester, name='notifications'),
    path('test-make/', make_notification, name='test-make'),

    path('import-mh-dm/', views.import_monhoc_dm, name='import_monhoc_dm'),
    path('import-lopsv/<int:lop_id>/', views.import_lopsv, name='import_lopsv'),
    path('export-sv/<int:lop_id>/', views.export_lopsv, name='export_lopsv'),
    path('import-gv/', views.import_gv, name='import_gv'),
    path('import-ns/', views.import_ns, name='import_ns'),
    path('export-gv/', views.export_gv, name='export_gv'),
    path('export-lh/', views.export_lh, name='export_lh'),

    path('report_hs81/<int:opt>/', views_report.report_hs81, name='report_hs81'),
    path('report_ttgv/<int:opt>/', views_report.report_ttgv, name='report_ttgv'),
    path('report_kqht/<int:opt>/', views_report.report_kqht, name='report_kqht'),
    path('report_dd/<int:opt>/', views_report.report_dd, name='report_dd'),
    path('thongbao/', views_report.tb_list, name='tb_list'),

    path('export_hs81/', views_report.export_hs81, name='export_hs81'),
    path('import_hs81/<int:lop_id>/', views_report.import_hs81, name='import_hs81'),
    path('import_hp81/<int:lop_id>/', views_report.import_hp81, name='import_hp81'),
    path('import_diemtp/<int:lop_id>/<int:lmh_id>/<int:ld_id>/', views_report.import_diemtp, name='import_diemtp'),
    path('import_edit_diemtp/<int:lop_id>/<int:lmh_id>/<int:ld_id>/<int:log_id>/', views_report.import_edit_diemtp, name='import_edit_diemtp'),
 
    path('allctdt/', views.ctdt_list, name='ctdt_list'),
#    path('alllop/', views.lop_list, name='lop_list'),
    path('alllop/', views.lop_list_guardian, name='lop_list'),
    path('allxlop/', views.xlop_list_guardian, name='xlop_list'),
    path('alllichhoc/', views.lichhoc_list, name='lichhoc_list'),
    path('registration/', views.create_lichhoc, name='create_lichhoc'),
    path('CreateLichhoclm/<int:lopmh_id>/', views.create_lichhoclm, name='create_lichhoclm'),
    path('lopsv/<int:lop_id>/', views.sv_lop, name='svlop_list'),
    path('lichhoc/<int:lop_id>/', views.lichhoc_lop, name='lichhoclop_list'),
    path('lichhoclmh/<int:lopmh_id>/', views.lichhoc_lopmh, name='lichhoclopmh_list'),
    path('hocphi/<int:lop_id>/', views.hocphi_lop, name='hocphi_list'),

    path('hp81/<int:sv_id>/<int:lop_id>/', views.hv_hp81_list, name='hv_hp81_list'),
    path('hp81-new/<int:lop_id>/', views.hv_hp81_new_list, name='hv_hp81_new_list'),

    path('hs_81/<int:sv_id>/<int:lop_id>/', views.hv_hs81_list, name='hv_hs81_list'),
    path('hs_81-new/<int:lop_id>/', views.hv_hs81_new_list, name='hv_hs81_new_list'),

#    path('monhoc/<int:lop_id>/', views.lop_monhoc, name='lop_monhoc'),
    path('monhoc/<int:lop_id>/', views.lop_monhoc_testwithGuardian, name='lop_monhoc'),
    path('<int:ctdt_id>/', views.single_ctdtmonhoc, name='lop_ctdtmonhoc'),
    path('ctdt_monhoc/<int:ctdt_id>/', views.ctdt_monhoc, name='ctdt_monhoc'),
    path('<int:ctdt_id>/', views.single_ctdtmonhoc, name='single_ctdtmonhoc'),
    path('CreateDiemdanh/<int:lh_id>', views.create_diemdanh, name='create_diemdanh'),
    path('CreateHocphi/<int:lh_id>', views.create_hocphi, name='create_hocphi'),

    path('CreateHp81/<int:lop_id>/<int:sv_id>', views.create_hp81, name='create_hp81'),
    path('EditHp81/<int:lop_id>/<int:hp81_id>', views.edit_hp81, name='edit_hp81'),
    path('CreateHs81/<int:lop_id>/<int:sv_id>', views.create_hs81, name='create_hs81'),
    path('EditHs81/<int:lop_id>/<int:hs81_id>', views.edit_hs81, name='edit_hs81'),

    path('CreateCtdtMonhoc/', views.create_ctdtmonhoc, name='create_ctdtmonhoc'),
    path('CreateLopMonhoc/<int:lop_id>/', views.create_lopmonhoc, name='create_lopmonhoc'),
    path('EditLopMonhoc/<int:lmh_id>/', views.edit_lopmonhoc, name='edit_lopmonhoc'),
    path('HistoryLopMonhoc/<int:lmh_id>/', views.history_lopmonhoc, name='history_lopmonhoc'),
    path('EditLichhoc/<int:lh_id>/', views.edit_lichhoc, name='edit_lichhoc'),

    path('CreateDiem/<int:lh_id>/', views.create_diem, name='create_diem'),
    path('CreateLop/', views.create_lop, name='create_lop'),
    path('CreatexLop/', views.create_xlop, name='create_xlop'),
    path('EditLop/<int:lop_id>/', views.edit_lop, name='edit_lop'),
    path('EditLop-new/<int:lop_id>/', views.edit_lop_new, name='edit_lop_new'),
    path('Lophk-list/<int:lop_id>/<int:lhk_id>/', views.lophk_list, name='lophk_list'),

    path('CreateSinhvien/', views.create_sv, name='create_sv'),
    path('EditSinhvien/<int:sv_id>/', views.edit_sv, name='edit_sv'),
    path('detailsSinhvien/<int:sv_id>/<int:opt>/', views.details_sv, name='details_sv'),
    path('CreateGiaovien/', views.create_gv, name='create_gv'),
    path('EditGiaovien/<int:gv_id>/', views.edit_gv, name='edit_gv'),
    path('detailsGiaovien/<int:gv_id>/', views.details_gv, name='details_gv'),
    path('Createnhansu/', views.create_ns, name='create_ns'),
    path('Editnhansu/<int:ns_id>/', views.edit_ns, name='edit_ns'),
    path('EditTtgv/<int:lop_id>/<int:lopmh_id>/<int:gv_id>/', views.edit_ttgv, name='edit_ttgv'),
    path('CreateCtdt/', views.create_ctdt, name='create_ctdt'),
    path('<int:teacher_id>/', views.single_teacher, name='single_teacher'),
    path('hs81/<int:lop_id>/', views.single_hs81lop, name='single_hs81lop'),
    path('lop81-lst/<int:lop_id>/', views.lop81_lst, name='lop81-lst'),
    path('diemdanh/<int:lh_id>', views.diemdanh_lop ,name='diemdanh_list'),
    path('registration/', views.create_teacher, name='create_teacher'),
    path('edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
    path('alldiem/<int:lop_id>/', views.diem_lop, name='diem-lop_list'),
    path('diemlmh/<int:lmh_id>/', views.diem_lmh, name='diem-lmh'),
    path('diemlmh-lst/<int:lmh_id>/', views.diem_lmh_lst, name='diem-lmh-lst'),
    path('diemtplmh-lst/<int:lmh_id>/', views.diemtp_lmh_lst, name='diemtp-lmh-lst'),
    path('detailsDtp/<int:lop_id>/<int:lmh_id>/', views.details_diemtp, name='details_diemtp'),

    path('gvlmh-lst/<int:lmh_id>/', views.gv_lmh_lst, name='gv-lmh-lst'),
    path('diemlmh-dtp/<int:lmh_id>/<int:dtp_id>/', views.diem_lmh_dtp, name='diem-lmh-dtp'),
    path('CreateDiemTP/<int:lop_id>/<int:lmh_id>/<int:dtp_id>/', views.create_diemtp, name='create_diemtp'),
    path('EditDiemTP/<int:lop_id>/<int:lmh_id>/<int:dtp_id>/<int:log_id>/', views.edit_diemtp, name='edit_diemtp'),
    path('DeleteDiemTP/<int:lop_id>/<int:lmh_id>/<int:dtp_id>/<int:log_id>/', views.delete_diemtp, name='delete_diemtp'),
    path('lop81-hk/<int:lop_id>/<int:hk_ma>/', views.lop81_hk, name='lop81-hk'),
    path('lophp-hk/<int:lop_id>/<int:hk_ma>/', views.lophp_hk, name='lophp-hk'),
    path('delete/<int:teacher_id>', views.delete_teacher, name='delete_teacher'),
    path('react', views.react, name='react'),

    path('upload/', views.upload_file, name='upload_file'),
    path('upload-gv/<int:gv_id>/', views.upload_file_gv, name='upload_file_gv'),
    path('upload-sv/<int:hv_id>/', views.upload_file_hv, name='upload_file_hv'),
    path('upload-lmh/<int:lmh_id>/', views.upload_file_lmh, name='upload_file_lmh'),

    path('download-temp/<int:file_id>/', views.download_file, name='download_file'),
    path('view-file/<int:file_id>/', views.view_file, name='view_file'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-file-gv/<int:gv_id>/<int:file_id>/', views.delete_file_gv, name='delete_file_gv'),
    path('delete-file-hv/<int:hv_id>/<int:file_id>/', views.delete_file_hv, name='delete_file_hv'),
    path('delete-file-lmh/<int:lmh_id>/<int:file_id>/', views.delete_file_lmh, name='delete_file_lmh'),
    path('download-temp1/', views.download_file1, name='download_file1'),
    path('download-temp2/', views.download_file2, name='download_file2'),

    path('add-ns/<int:id>/', add_nsuser, name='add_ns'),
    path('resetpwd/<int:ns_id>/', reset_pwd, name='reset_pwd'),

    path('add-gv/<int:id>/', add_gvuser, name='add_gv'),
    path('resetpwd-gv/<int:gv_id>/', reset_pwd_gv, name='reset_pwd_gv'),

    path('add-hv/<int:id>/', add_hvuser, name='add_hv'),
    path('resetpwd-hv/<int:hv_id>/', reset_pwd_hv, name='reset_pwd_hv'),

    path('changepwd/', user_changepwd, name='changepwd'),
 
    path('create_tbs/', create_tbs, name='create_tbs'),
]
admin.site.site_url = None
admin.site.site_header = 'My Site'
