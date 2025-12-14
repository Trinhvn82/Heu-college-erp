from django.urls import path

from .views import forum_list, forum_create, forum_detail

urlpatterns = [
    path('', forum_list, name='forum_list'),
    path('create/', forum_create, name='forum_create'),
    path('<int:post_id>/', forum_detail, name='forum_detail'),
]
