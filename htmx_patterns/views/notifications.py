''' Django notifications views for tests '''
# -*- coding: utf-8 -*-
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from notifications.signals import notify


@login_required

def owner_notifications(request):
    """View notification cho chủ nhà"""
    notify.send(sender=request.user, recipient=request.user, verb='Bạn đã mở trang thông báo (chủ nhà)', level='info')
    return render(request, 'sms/owner_notifications.html', {
        'unread_count': request.user.notifications.unread().count(),
        'notifications': request.user.notifications.all(),
        'is_owner': True
    })

def renter_notifications(request):
    """View notification cho renter"""
    notify.send(sender=request.user, recipient=request.user, verb='Bạn đã mở trang thông báo (renter)', level='info')
    return render(request, 'sms/renter_notifications.html', {
        'unread_count': request.user.notifications.unread().count(),
        'notifications': request.user.notifications.all(),
        'is_renter': True
    })

def live_tester(request):
    notify.send(sender=request.user, recipient=request.user, verb='you loaded the page', level='success')
    #('success', 'info', 'warning', 'error') (default=info)
    return render(request, 'sms/test_live.html', {
        'unread_count': request.user.notifications.unread().count(),
        'notifications': request.user.notifications.all()
    })


def make_notification(request):

    the_notification = random.choice([
        'reticulating splines',
        'cleaning the car',
        'jumping the shark',
        'testing the app',
        'attaching the plumbus',
    ])

    notify.send(sender=request.user, recipient=request.user,
                verb='you asked for a notification - you are ' + the_notification)
