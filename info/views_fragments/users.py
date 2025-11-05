from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model

@login_required
@permission_required('auth.view_user')
def user_list_view(request):
    User = get_user_model()
    users = User.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'sms/user_list.html', context)