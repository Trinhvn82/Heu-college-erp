from django.urls import path, include, register_converter
from . import views, views_report, views_htmx
from django.contrib import admin
from info.views import *

from htmx_patterns.views.restarts import view_restart, view_search
from htmx_patterns.views.thongbao import view_tb, view_tb_search 
from htmx_patterns.views.monhoc import view_mh, view_mh_search 
from htmx_patterns.views.gv_lmh import view_gv_lmh_search, view_gv_lmh 

from htmx_patterns.views.notifications import live_tester, make_notification
from sms.tasks import create_tbs
from . import views as sms_views
from sms.utils.hashid_converter import HashidConverter

# Register custom URL converter for hashids (encoded integer IDs)
register_converter(HashidConverter, 'hashid')

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome-page/', views.welcome_page, name='welcome_page'),
    path('home/', views.home_dashboard, name='home_dashboard'),
    path('welcome/', views.renter_landing, name='renter_landing'),
    path('renter/dashboard/', views.renter_dashboard, name='renter_dashboard'),
    path('renter/bills/', views.renter_bills, name='renter_bills'),
    path('renter/locations/', views.renter_locations, name='renter_locations'),
    path('renter/contracts/', views.renter_contracts, name='renter_contracts'),
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

    # path('gv_lmh_htmx/<int:gv_id>/', view_restart, name='gv_lmh_htmx'),
    # path('search_lmh_htmx/<int:gv_id>/', view_search, name='search_lmh_htmx'),

    path('tb_htmx/', view_tb, name='tb_list_htmx'),
    path('search_tb_htmx/', view_tb_search, name='search_tb_htmx'),

    path('mh_htmx/<int:ctdt_id>/', view_mh, name='mh_list_htmx'),
    path('search_mh_htmx/<int:ctdt_id>/', view_mh_search, name='search_mh_htmx'),

    path('gv_lmh_htmx/<int:gv_id>/', view_gv_lmh, name='gv_lmh_htmx'),
    path('search_gv_lmh_htmx/<int:gv_id>/', view_gv_lmh_search, name='search_gv_lmh_htmx'),

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
    path('report_td/<int:opt>/', views_report.report_td, name='report_td'),
    path('report_tn/', views_report.report_tn, name='report_tn'),
    path('thongbao/', views_report.tb_list, name='tb_list'),

    path('export_hs81/', views_report.export_hs81, name='export_hs81'),
    path('import_hs81/<int:lop_id>/', views_report.import_hs81, name='import_hs81'),
    path('import_hp81/<int:lop_id>/', views_report.import_hp81, name='import_hp81'),
    path('import_diemtp/<int:lop_id>/<int:lmh_id>/<int:ld_id>/', views_report.import_diemtp, name='import_diemtp'),
    path('import_edit_diemtp/<int:lop_id>/<int:lmh_id>/<int:ld_id>/<int:log_id>/', views_report.import_edit_diemtp, name='import_edit_diemtp'),
 
    path('allctdt/', views.ctdt_list, name='ctdt_list'),
#    path('alllop/', views.lop_list, name='lop_list'),
    path('index/', views.index1, name='index1'),
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
    path('hp81-hk/<int:lop_id>/', views.hv_hp81_hk_list, name='hv_hp81_hk_list'),

    path('hs_81/<int:sv_id>/<int:lop_id>/', views.hv_hs81_list, name='hv_hs81_list'),
    path('hs_81-new/<int:lop_id>/', views.hv_hs81_new_list, name='hv_hs81_new_list'),
    path('hs_81-hk/<int:lop_id>/', views.hv_hs81_hk_list, name='hv_hs81_hk_list'),

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
   path('hoclai/<int:lmh_id>/', views.hoclai_list, name='hoclai_list'),
 
    path('CreateDiem/<int:lh_id>/', views.create_diem, name='create_diem'),
    path('CreateLop/', views.create_lop, name='create_lop'),
    path('CreatexLop/', views.create_xlop, name='create_xlop'),
    path('EditLop/<int:lop_id>/', views.edit_lop, name='edit_lop'),
    path('EditLop-new/<int:lop_id>/', views.edit_lop_new, name='edit_lop_new'),
    path('Lophk-list/<int:lop_id>/<int:lhk_id>/', views.lophk_list, name='lophk_list'),

     path('allloc/', views.loc_list, name='loc_list'),
     path('CreateLoc/', views.create_loc, name='create_loc'),
     path('EditLoc/<int:loc_id>/', views.edit_loc, name='edit_loc'),
     # Secure Location CRUD (parallel)
     path('EditLoc/<hashid:loc_id>/', views.edit_loc, name='edit_loc_secure'),

     path('allhouse/<int:loc_id>/', views.house_list, name='house_list'),
     path('CreateHouse/<int:loc_id>/', views.create_house, name='create_house'),
     path('EditHouse/<int:loc_id>/<int:house_id>/', views.edit_house, name='edit_house'),
     # Secure House CRUD (parallel)
     path('allhouse/<hashid:loc_id>/', views.house_list, name='house_list_secure'),
     path('CreateHouse/<hashid:loc_id>/', views.create_house, name='create_house_secure'),
     path('EditHouse/<hashid:loc_id>/<hashid:house_id>/', views.edit_house, name='edit_house_secure'),

     path('CreateRenter/', views.create_renter, name='create_renter'),
     path('EditRenter/<int:renter_id>/', views.edit_renter, name='edit_renter'),
     path('allRenter/', views.renter_list, name='renter_list'),
     # Secure Renter CRUD (parallel)
     path('EditRenter/<hashid:renter_id>/', views.edit_renter, name='edit_renter_secure'),

    #path('allhouserenter/<int:loc_id>/', views.houserenter_list, name='houserenter_list'),
    #path('CreateHouseRenter/<int:loc_id>/', views.create_houserenter, name='create_houserenter'),
    #path('EditHouseRenter/<int:id>/', views.edit_houserenter, name='edit_houserenter '),

    path('CreateSinhvien/', views.create_sv, name='create_sv'),
    path('EditSinhvien/<int:sv_id>/', views.edit_sv, name='edit_sv'),
     # Secure Student edit (parallel)
     path('EditSinhvien/<hashid:sv_id>/', views.edit_sv, name='edit_sv_secure'),
    path('detailsSinhvien/<int:sv_id>/<int:opt>/', views.details_sv, name='details_sv'),
     # Secure Student details (parallel)
     path('detailsSinhvien/<hashid:sv_id>/<int:opt>/', views.details_sv, name='details_sv_secure'),
    path('CreateGiaovien/', views.create_gv, name='create_gv'),
    path('EditGiaovien/<int:gv_id>/', views.edit_gv, name='edit_gv'),
    path('detailsGiaovien/<int:gv_id>/', views.details_gv, name='details_gv'),
    path('Createnhansu/', views.create_ns, name='create_ns'),
    path('Editnhansu/<int:ns_id>/', views.edit_ns, name='edit_ns'),
    path('EditTtgv/<int:lop_id>/<int:lopmh_id>/<int:gv_id>/', views.edit_ttgv, name='edit_ttgv'),
    path('CreateCtdt/', views.create_ctdt, name='create_ctdt'),
    path('<int:teacher_id>/', views.single_teacher, name='single_teacher'),
     # Secure Teacher detail (parallel)
     path('<hashid:teacher_id>/', views.single_teacher, name='single_teacher_secure'),
    path('hs81/<int:lop_id>/', views.single_hs81lop, name='single_hs81lop'),
    path('lop81-lst/<int:lop_id>/', views.lop81_lst, name='lop81-lst'),
    path('diemdanh/<int:lh_id>', views.diemdanh_lop ,name='diemdanh_list'),
    path('registration/', views.create_teacher, name='create_teacher'),
    path('edit/<int:pk>', views.edit_teacher, name='edit_teacher'),
     # Secure Teacher edit (parallel)
     path('edit/<hashid:pk>', views.edit_teacher, name='edit_teacher_secure'),
    path('alldiem/<int:lop_id>/', views.diem_lop, name='diem-lop_list'),
    path('diemlmh/<int:lmh_id>/', views.diem_lmh, name='diem-lmh'),
    path('diemlmh-lst/<int:lmh_id>/', views.diem_lmh_lst, name='diem-lmh-lst'),
    path('diemtplmh-lst/<int:lmh_id>/<int:opt>/', views.diemtp_lmh_lst, name='diemtp-lmh-lst'),
    path('detailsDtp/<int:lop_id>/<int:lmh_id>/', views.details_diemtp, name='details_diemtp'),

    path('gvlmh-lst/<int:lmh_id>/', views.gv_lmh_lst, name='gv-lmh-lst'),
    path('diemlmh-dtp/<int:lmh_id>/<int:dtp_id>/', views.diem_lmh_dtp, name='diem-lmh-dtp'),
    path('CreateDiemTP/<int:lop_id>/<int:lmh_id>/<int:dtp_id>/', views.create_diemtp, name='create_diemtp'),
    path('EditDiemTP/<int:lop_id>/<int:lmh_id>/<int:dtp_id>/<int:log_id>/', views.edit_diemtp, name='edit_diemtp'),
    path('DeleteDiemTP/<int:lmh_id>/<int:dtp_id>/<int:log_id>/', views.delete_diemtp, name='delete_diemtp'),
    path('lop81-hk/<int:lop_id>/<int:hk_ma>/', views.lop81_hk, name='lop81-hk'),
    path('lophp-hk/<int:lop_id>/<int:hk_ma>/', views.lophp_hk, name='lophp-hk'),
    path('delete/<int:teacher_id>', views.delete_teacher, name='delete_teacher'),
     # Secure Teacher delete (parallel)
     path('delete/<hashid:teacher_id>', views.delete_teacher, name='delete_teacher_secure'),
    path('react', views.react, name='react'),

    path('upload/', views.upload_file, name='upload_file'),
    path('upload-gv/<int:gv_id>/', views.upload_file_gv, name='upload_file_gv'),
    path('upload-sv/<int:hv_id>/', views.upload_file_hv, name='upload_file_hv'),
    path('upload-lmh/<int:lmh_id>/', views.upload_file_lmh, name='upload_file_lmh'),

     path('upload-loc/<int:loc_id>/', views.upload_file_loc, name='upload_file_loc'),
      path('view-loc/<int:loc_id>/', views.view_loc, name='view_loc'),
      # Secure Location file/view routes
      path('upload-loc/<hashid:loc_id>/', views.upload_file_loc, name='upload_file_loc_secure'),
      path('view-loc/<hashid:loc_id>/', views.view_loc, name='view_loc_secure'),
      path('view-house/<hashid:house_id>/', views.view_house, name='view_house_secure'),
     path('houses/', views.houses, name='houses'),
     path('houses/partial/', views.houses_partial, name='houses_partial'),
     path('create-hr/<int:id>/', views.create_hr, name='create_hr'),
    path('hr-list/<int:id>/', views.hr_list, name='hr_list'),
     path('hr-list-partial/<int:id>/', views.hr_list_partial, name='hr_list_partial'),
     path('hr-toggle-active/<int:hr_id>/', views.hr_toggle_active, name='hr_toggle_active'),
     path('hr-delete/<int:hr_id>/', views.hr_delete, name='hr_delete'),
          # Secure HR/Contract routes
          path('create-hr/<hashid:id>/', views.create_hr, name='create_hr_secure'),
          path('hr-list/<hashid:id>/', views.hr_list, name='hr_list_secure'),
          path('hr-list-partial/<hashid:id>/', views.hr_list_partial, name='hr_list_partial_secure'),
          path('hr-toggle-active/<hashid:hr_id>/', views.hr_toggle_active, name='hr_toggle_active_secure'),
          path('hr-delete/<hashid:hr_id>/', views.hr_delete, name='hr_delete_secure'),
                # Contract detail & listing (new secure routes)
                path('contract/<hashid:contract_id>/', views.contract_detail, name='contract_detail_secure'),
                path('house/<hashid:house_id>/contracts/', views.house_contracts, name='house_contracts_secure'),
                # Legacy naming aliases on same hash paths
                path('contract/<hashid:contract_id>/', views.contract_detail, name='contract_detail'),
                path('house/<hashid:house_id>/contracts/', views.house_contracts, name='house_contracts'),
  #  path('upload-house/<int:house_id>/', views.upload_file_house, name='upload_file_house'),

    path('hoclai-lmh/<int:lmh_id>/', views.hoclai_list, name='hoclai_list'),
    path('delete-hoclai/<int:lmh_id>/<int:sv_id>/', views.delete_hoclai, name='delete_hoclai'),

    path('download-temp/<int:file_id>/', views.download_file, name='download_file'),
    path('view-file/<int:file_id>/', views.view_file, name='view_file'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-file-gv/<int:gv_id>/<int:file_id>/', views.delete_file_gv, name='delete_file_gv'),
    path('delete-file-hv/<int:hv_id>/<int:file_id>/', views.delete_file_hv, name='delete_file_hv'),
    path('delete-file-lmh/<int:lmh_id>/<int:file_id>/', views.delete_file_lmh, name='delete_file_lmh'),
     path('delete-file-loc/<int:loc_id>/<int:file_id>/', views.delete_file_loc, name='delete_file_loc'),
     path('delete-file-loc/<hashid:loc_id>/<hashid:file_id>/', views.delete_file_loc, name='delete_file_loc_secure'),
    path('download-temp1/', views.download_file1, name='download_file1'),
    path('download-temp2/', views.download_file2, name='download_file2'),

    path('download-temp-diem/<int:lmh_id>/', views.download_temp_diem, name='download_temp_diem'),
    path('download-template/<int:opt>/', views.download_temp, name='download_temp'),
    path('download-tpl-data/<int:lop_id>/<int:opt>/', views.download_temp_data, name='download_temp_data'),

    path('add-ns/<int:id>/', add_nsuser, name='add_ns'),
    path('resetpwd/<int:ns_id>/', reset_pwd, name='reset_pwd'),

    path('add-gv/<int:id>/', add_gvuser, name='add_gv'),
    path('resetpwd-gv/<int:gv_id>/', reset_pwd_gv, name='reset_pwd_gv'),

    path('add-hv/<int:id>/', add_hvuser, name='add_hv'),
    path('resetpwd-hv/<int:hv_id>/', reset_pwd_hv, name='reset_pwd_hv'),
     # Secure student user actions (parallel)
     path('add-hv/<hashid:id>/', add_hvuser, name='add_hv_secure'),
     path('resetpwd-hv/<hashid:hv_id>/', reset_pwd_hv, name='reset_pwd_hv_secure'),

    path('add-renter/<int:id>/', add_renteruser, name='add_renter'),
    path('toggle-renter/<int:renter_id>/', toggle_renter_status, name='toggle_renter_status'),
    path('resetpwd-renter/<int:renter_id>/', reset_pwd_renter, name='reset_pwd_renter'),
     # Secure renter actions
     path('add-renter/<hashid:id>/', add_renteruser, name='add_renter_secure'),
     path('toggle-renter/<hashid:renter_id>/', toggle_renter_status, name='toggle_renter_status_secure'),
     path('resetpwd-renter/<hashid:renter_id>/', reset_pwd_renter, name='reset_pwd_renter_secure'),

    path('changepwd/', user_changepwd, name='changepwd'),
 
    path('signup/', signup, name='signup'),
    path('signup/success/', signup_success, name='signup_success'),

    path('create_tbs/', create_tbs, name='create_tbs'),

    #HTMX
    path("lichhoc-new/", views_htmx.lichhoc_list, name='lichhoc_list-new'),
    path("search-lh/", views_htmx.search_lh, name='search-lh'),
    path('get-lichhoc/', views_htmx.get_lichhoc, name='get-lichhoc'),

     #bill
    # DEPRECATED integer-ID routes (Phase 2): kept commented for reference
    # path('location/<int:loc_id>/bills/', views.bill_list_view, name='bill_list'),
    # path('house/<int:house_id>/create-bill/', views.create_bill_view, name='create_bill'),
    # path('bill/<int:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
    # path('bill/<int:bill_id>/comment/', sms_views.add_bill_comment, name='add_bill_comment'),
    # path('bill/<int:bill_id>/update/', views.update_bill_view, name='update_bill'),
    # path('bill/<int:bill_id>/add-payment/', views.add_payment, name='add_payment'),
    # path('payment/confirm/<int:payment_id>/', views.confirm_payment_view, name='confirm_payment'),
    # path('payment/delete/<int:payment_id>/', views.delete_payment_view, name='delete_payment'),
    # path('bill/<int:bill_id>/upload-file/', views.upload_bill_file, name='upload_bill_file'),
     # invoice search
     path('invoices/search/', views.invoice_search, name='invoice_search'),
     path('invoices/export-excel/', views.invoice_export_excel, name='invoice_export_excel'),
     path('api/locations/<int:loc_id>/houses/', views.api_houses_by_location, name='api_houses_by_location'),
    #path('bill/<int:bill_id>/excel/', views.generate_bill_excel, name='generate_bill_excel'),
    path('bill/<int:bill_id>/pdf/', views.generate_bill_pdf, name='generate_bill_pdf'),

     # Secure (encoded ID) routes — now canonical
     # Bills (encoded bill_id)
     path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail_secure'),
     path('bill/<hashid:bill_id>/update/', views.update_bill_view, name='update_bill_secure'),
     path('bill/<hashid:bill_id>/add-payment/', views.add_payment, name='add_payment_secure'),
     path('bill/<hashid:bill_id>/upload-file/', views.upload_bill_file, name='upload_bill_file_secure'),
     path('bill/<hashid:bill_id>/pdf/', views.generate_bill_pdf, name='generate_bill_pdf_secure'),
     path('bill/<hashid:bill_id>/comment/', views.add_bill_comment, name='add_bill_comment_secure'),
     # Backward-compatibility aliases (hashid paths with legacy names)
     path('bill/<hashid:bill_id>/detail/', views.bill_detail_view, name='bill_detail'),
     path('bill/<hashid:bill_id>/update/', views.update_bill_view, name='update_bill'),
     path('bill/<hashid:bill_id>/add-payment/', views.add_payment, name='add_payment'),
     path('bill/<hashid:bill_id>/upload-file/', views.upload_bill_file, name='upload_bill_file'),
     path('bill/<hashid:bill_id>/pdf/', views.generate_bill_pdf, name='generate_bill_pdf'),
     path('bill/<hashid:bill_id>/comment/', views.add_bill_comment, name='add_bill_comment'),
     # Payment (encoded payment_id)
     path('payment/confirm/<hashid:payment_id>/', views.confirm_payment_view, name='confirm_payment_secure'),
     path('payment/delete/<hashid:payment_id>/', views.delete_payment_view, name='delete_payment_secure'),
     # Backward-compatibility aliases (hashid paths with legacy names)
     path('payment/confirm/<hashid:payment_id>/', views.confirm_payment_view, name='confirm_payment'),
     path('payment/delete/<hashid:payment_id>/', views.delete_payment_view, name='delete_payment'),
     # Location/House (encoded)
     path('location/<hashid:loc_id>/bills/', views.bill_list_view, name='bill_list_secure'),
     path('house/<hashid:house_id>/create-bill/', views.create_bill_view, name='create_bill_secure'),
     # Legacy names on hashid paths
     path('location/<hashid:loc_id>/bills/', views.bill_list_view, name='bill_list'),
     path('house/<hashid:house_id>/create-bill/', views.create_bill_view, name='create_bill'),

     # Notifications & Issues
     path('notifications/list/', sms_views.notifications_list, name='notifications_list'),
     path('notifications/badge/', sms_views.notification_badge, name='notification_badge'),
     # Integer notification route deprecated in favor of hashid
     # path('notifications/<int:notification_id>/read/', sms_views.mark_notification_read, name='mark_notification_read'),
     # Renter issues
     path('renter/issues/', sms_views.renter_issue_list, name='renter_issues'),
     path('issues/report/', sms_views.renter_report_issue, name='renter_report_issue'),
     # Landlord issues
     path('issues/', sms_views.issue_list, name='issue_list'),
     # Keep integer Issue routes temporarily for backward compatibility with old notifications (to be removed later)
     path('issues/<int:issue_id>/', sms_views.issue_detail, name='issue_detail_int_deprecated'),
     path('issues/<int:issue_id>/modal/', sms_views.issue_detail_modal, name='issue_detail_modal_int_deprecated'),
     path('issues/<int:issue_id>/comment/', sms_views.add_issue_comment, name='add_issue_comment_int_deprecated'),
     path('issues/<int:issue_id>/status/', sms_views.change_issue_status, name='change_issue_status_int_deprecated'),
     path('issues/<int:issue_id>/resolve/', sms_views.resolve_issue, name='resolve_issue_int_deprecated'),
     path('issues/<int:issue_id>/confirm/', sms_views.renter_confirm_issue, name='renter_confirm_issue_int_deprecated'),
     path('issues/bulk-status/', sms_views.bulk_change_issue_status, name='bulk_change_issue_status'),

     # Secure (encoded) Issue/Notification routes
     path('notifications/<hashid:notification_id>/read/', sms_views.mark_notification_read, name='mark_notification_read_secure'),
     # Legacy name alias
     path('notifications/<hashid:notification_id>/read/', sms_views.mark_notification_read, name='mark_notification_read'),
     path('issues/<hashid:issue_id>/', sms_views.issue_detail, name='issue_detail_secure'),
     path('issues/<hashid:issue_id>/modal/', sms_views.issue_detail_modal, name='issue_detail_modal_secure'),
     path('issues/<hashid:issue_id>/comment/', sms_views.add_issue_comment, name='add_issue_comment_secure'),
     path('issues/<hashid:issue_id>/status/', sms_views.change_issue_status, name='change_issue_status_secure'),
     path('issues/<hashid:issue_id>/resolve/', sms_views.resolve_issue, name='resolve_issue_secure'),
     path('issues/<hashid:issue_id>/confirm/', sms_views.renter_confirm_issue, name='renter_confirm_issue_secure'),
     # Legacy names on hashid paths (so reverse('issue_detail') uses hashid)
     path('issues/<hashid:issue_id>/', sms_views.issue_detail, name='issue_detail'),
     path('issues/<hashid:issue_id>/modal/', sms_views.issue_detail_modal, name='issue_detail_modal'),
     path('issues/<hashid:issue_id>/comment/', sms_views.add_issue_comment, name='add_issue_comment'),
     path('issues/<hashid:issue_id>/status/', sms_views.change_issue_status, name='change_issue_status'),
     path('issues/<hashid:issue_id>/resolve/', sms_views.resolve_issue, name='resolve_issue'),
     path('issues/<hashid:issue_id>/confirm/', sms_views.renter_confirm_issue, name='renter_confirm_issue'),
]
admin.site.site_url = None
admin.site.site_header = 'My Site'
