from .models import CustomUser, Job, Application,Seeker,SeekerNotification
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def employer_notification_count(request):
    if request.user.is_authenticated and request.user.user_type == "2":
        jobs = Job.objects.filter(employer__user=request.user)
        count = Application.objects.filter(
            job__in=jobs,
            status='Applied'
        ).count()
    else:
        count = 0

    return {'employer_notification_count': count}


@login_required
def admin_notifications(request):

    pending_users = CustomUser.objects.filter(
        status=0
    ).exclude(user_type="1")

    pending_jobs = Job.objects.filter(status=0)

    new_applications = Application.objects.filter(status='Applied')

    return render(request, 'admin_notifications.html', {
        'pending_users': pending_users,
        'pending_jobs': pending_jobs,
        'new_applications': new_applications
    })

def admin_notification_count(request):
    if request.user.is_authenticated and request.user.user_type == "1":
        pending_users = CustomUser.objects.filter(
            status=0
        ).exclude(user_type="1").count()

        pending_jobs = Job.objects.filter(status=0, admin_seen=False).count()

        new_applications = Application.objects.filter(
    status='Applied',
    admin_seen=False
).count()

        total_notifications = (
            pending_users +
            pending_jobs +

            
            new_applications
        )

        return {
            'admin_notification_count': total_notifications
        }

    return {}



def seeker_notification_count(request):
    if request.user.is_authenticated and request.user.user_type == "3":
        seeker = Seeker.objects.get(user=request.user)
        count = SeekerNotification.objects.filter(
            seeker=seeker,
            is_read=False
        ).count()
        return {'seeker_notification_count': count}
    return {}
