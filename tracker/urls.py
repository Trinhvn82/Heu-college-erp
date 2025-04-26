from django.urls import path
from tracker import views


urlpatterns = [
#    path("", views.index, name='index'),
    path("transactions/", views.transactions_list, name='transactions-list'),
    path("lichhoc-new/", views.lichhoc_list, name='lichhoc_list-new'),
    path("search-lh/", views.search_lh, name='search-lh'),
    path('transactions/create/', views.create_transaction, name='create-transaction'),

    path('transactions/<int:pk>/update/', views.update_transaction, name='update-transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete-transaction'),

    path('get-lichhoc/', views.get_lichhoc, name='get-lichhoc'),

    path('transactions/charts', views.transaction_charts, name='transactions-charts'),

    path('transactions/export', views.export, name='export'),
    path('transactions/import', views.import_transactions, name='import'),
]
