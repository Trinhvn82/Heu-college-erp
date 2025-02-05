from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
    path('diemdanh', views.report_diemdanh, name='report_diemdanh'),
    path('api-hssv', views.api_hssv, name='api_hssv'),
    path('chamcong', views.report_chamcong, name='report_chamcong'),
    path('hocphi', views.report_hocphi, name='report_hocphi'),
]
