import re
import random
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Seeker, Employer, CustomUser,Job,Application,SeekerNotificationPreference
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# @login_required
# def employerdash(request):
#     employer = Employer.objects.get(user=request.user)

#     # Total jobs
#     total_jobs = Job.objects.filter(employer=employer).count()

#     # Total applicants (all jobs)
#     total_applicants = Application.objects.filter(
#         job__employer=employer
#     ).count()

#     # Scheduled jobs = jobs whose last_date is in future
#     scheduled_jobs = Job.objects.filter(
#         employer=employer,
#         last_date__gte=timezone.now().date()
#     ).count()

#     # Jobs posted this week
#     week_start = timezone.now().date() - timedelta(days=7)
#     recent_jobs = Job.objects.filter(
#         employer=employer,
#         posted_date__gte=week_start
#     )

#     return render(request, 'employerdash.html', {
#         'total_jobs': total_jobs,
#         'total_applicants': total_applicants,
#         'scheduled_jobs': scheduled_jobs,
#         'recent_jobs': recent_jobs,
#     })

def home(request):
    return render(request, 'index.html')
def admindash(request):
    return render(request, 'admindash.html')
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def employerdash(request):
    employer = Employer.objects.get(user=request.user)

    total_jobs = Job.objects.filter(employer=employer).count()

    total_applicants = Application.objects.filter(
        job__employer=employer
    ).count()

    scheduled_jobs = Job.objects.filter(
        employer=employer,
        last_date__gte=timezone.now().date()
    ).count()

    # Jobs posted this week
    week_start = timezone.now().date() - timedelta(days=7)
    recent_jobs = Job.objects.filter(
        employer=employer,
        posted_date__gte=week_start
    )

    return render(request, 'employerdash.html', {
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'scheduled_jobs': scheduled_jobs,
        'recent_jobs': recent_jobs,
    })



import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.shortcuts import render, redirect

def seeker_reg(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        dob = request.POST['dob']
        user_type = int(request.POST['user_type'])

        # ✅ FIXED: STRICT EMAIL VALIDATION + DOMAIN WHITELIST
        try:
            from django.core.validators import validate_email
            validate_email(email)
            
            # ✅ DOMAIN WHITELIST (blocks abc@gm.com)
            domain = email.split('@')[1].lower()
            valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
                           'rediffmail.com', 'yahoo.co.in', 'gmail.co.in']
            
            if domain not in valid_domains:
                messages.error(request, "Use valid domains: gmail.com, yahoo.com, etc.")
                return render(request, 'seeker_reg.html')
                
        except:
            messages.error(request, "Invalid email format")
            return render(request, 'seeker_reg.html')

        # Mobile validation
        if not re.fullmatch(r'[6-9]\d{9}', mobile):
            messages.error(request, 'Enter valid 10-digit mobile number')
            return render(request, 'seeker_reg.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'seeker_reg.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'seeker_reg.html')

        if Seeker.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Mobile already registered')
            return render(request, 'seeker_reg.html')

        user = CustomUser.objects.create(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            user_type=user_type,
            status=0
        )

        seeker = Seeker.objects.create(
            user=user,
            mobile=mobile,
            dob=dob
        )

        SeekerNotificationPreference.objects.create(seeker=seeker)

        messages.success(request, 'Registration successful. Wait for admin approval.')
        return redirect('seeker_reg')

    return render(request, 'seeker_reg.html')




def employer_reg(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        company_name = request.POST['company_name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        logo = request.FILES.get('logo')
        user_type = int(request.POST['user_type'])

        # ✅ FIXED: STRICT EMAIL VALIDATION + DOMAIN WHITELIST
        try:
            from django.core.validators import validate_email
            validate_email(email)
            
            # ✅ DOMAIN WHITELIST (blocks abc@gm.com)
            domain = email.split('@')[1].lower()
            valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
                           'rediffmail.com', 'yahoo.co.in', 'gmail.co.in']
            
            if domain not in valid_domains:
                messages.error(request, "Use valid domains: gmail.com, yahoo.com, etc.")
                return render(request, 'employer_reg.html')
                
        except:
            messages.error(request, "Invalid email format")
            return render(request, 'employer_reg.html')

        if not re.fullmatch(r'[6-9]\d{9}', mobile):
            messages.error(request, 'Enter valid mobile number')
            return render(request, 'employer_reg.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'employer_reg.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'employer_reg.html')

        if Employer.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Mobile already registered')
            return render(request, 'employer_reg.html')

        user = CustomUser.objects.create(
            username=username,
            first_name=fname,
            last_name=lname,
            email=email,
            user_type=user_type,
            status=0
        )

        Employer.objects.create(
            user=user,
            company_name=company_name,
            mobile=mobile,
            address=address,
            logo=logo
        )

        messages.success(request, 'Registration successful. Wait for admin approval.')
        return redirect('employer_reg')

    return render(request, 'employer_reg.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.user_type == "1":
                login(request, user)
                return redirect('admindash')

            elif user.user_type == "2":
                login(request, user)
                return redirect('employerdash')

            elif user.user_type == "3":
                login(request, user)
                return redirect('seeker_dashboard')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login_view')

    return render(request, 'login.html')


def approve_disapprove(request):
    users = CustomUser.objects.filter(
        status=0
    ).exclude(user_type="1")   # exclude admin

    return render(
        request,
        'approveusers.html',
        {'users': users}
    )


def approve(request, k):
    usr = CustomUser.objects.get(id=k)
    usr.status = 1

    password = str(random.randint(100000, 999999))
    usr.set_password(password)
    usr.save()

    send_mail(
        'Job Portal Approval',
        f'Username: {usr.username}\nPassword: {password}',
        settings.EMAIL_HOST_USER,
        [usr.email]
    )

    messages.success(request, 'User approved and credentials sent')
    return redirect('approve_disapprove')


def disapprove(request, k):
    usr = CustomUser.objects.get(id=k)

    # 🔹 Save email before deleting
    email = usr.email
    username = usr.username
    user_type = usr.user_type

    # 🔹 Delete related profile
    if user_type == "2":
        Employer.objects.filter(user=usr).delete()
        role = "Employer"
    elif user_type == "3":
        Seeker.objects.filter(user=usr).delete()
        role = "Job Seeker"
    else:
        role = "User"

    # 🔹 Delete user
    usr.delete()

    # 🔹 SEND EMAIL
    send_mail(
        subject="Job Portal Registration Disapproved",
        message=f"""
Hello {username},

We regret to inform you that your {role} registration
on Job Portal has been disapproved by the admin.

If you believe this was a mistake, please contact support
or register again with valid information.

Regards,
Job Portal Team
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=True
    )

    return redirect('approve_disapprove')


def view_employers(request):
    employers = Employer.objects.filter(
        user__status=1,
        user__user_type="2"
    )
    return render(request, 'view_employers.html', {'employers': employers})
def delete_employer(request, user_id):
    user = CustomUser.objects.get(id=user_id, user_type="2")
    Employer.objects.filter(user=user).delete()
    user.delete()

    messages.success(request, "Employer deleted successfully")
    return redirect('view_employers')


def view_seekers(request):
    seekers = Seeker.objects.filter(
        user__status=1,
        user__user_type="3"
    )
    return render(request, 'view_seekers.html', {'seekers': seekers})
def delete_seeker(request, user_id):
    user = CustomUser.objects.get(id=user_id, user_type="3")
    Seeker.objects.filter(user=user).delete()
    user.delete()

    messages.success(request, "Job seeker deleted successfully")
    return redirect('view_seekers')




@login_required
def post_job(request):
    employer = Employer.objects.get(user=request.user)

    if request.method == "POST":
        designation = request.POST.get('designation', '').strip()
        description = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        last_date = request.POST.get('last_date')
        job_type = request.POST.get('job_type')

        # ================= VALIDATIONS =================

        # Job Designation
        if len(designation) < 3:
            messages.error(request, "Job designation must be at least 3 characters long.")
            return render(request, 'post_job.html')

        # Job Type
        if not job_type:
            messages.error(request, "Please select a job type.")
            return render(request, 'post_job.html')

        # Job Description
        if len(description) < 10:
            messages.error(
                request,
                "Job description must be at least 20 characters long."
            )
            return render(request, 'post_job.html')

        # Job Requirements
        if len(requirements) < 10:
            messages.error(
                request,
                "Job requirements must be at least 10 characters long."
            )
            return render(request, 'post_job.html')

        # Last date validation
        try:
            last_date_obj = date.fromisoformat(last_date)
            if last_date_obj < date.today():
                messages.error(request, "Last date cannot be in the past.")
                return render(request, 'post_job.html')
        except:
            messages.error(request, "Invalid last date.")
            return render(request, 'post_job.html')

        # ================= SAVE JOB =================
        Job.objects.create(
            employer=employer,
            designation=designation,
            description=description,
            requirements=requirements,
            job_type=job_type,
            last_date=last_date_obj
        )

        messages.success(request, "Job posted successfully and sent for admin approval.")
        return redirect('post_job')

    return render(request, 'post_job.html')


@login_required
def my_jobs(request):
    employer = Employer.objects.get(user=request.user)
    jobs = Job.objects.filter(employer=employer).order_by('-posted_date')
    return render(request, 'my_jobs.html', {'jobs': jobs})


@login_required
def delete_job(request, job_id):
    employer = Employer.objects.get(user=request.user)
    job = Job.objects.get(id=job_id, employer=employer)
    job.delete()
    messages.success(request, "Job deleted successfully")
    return redirect('my_jobs')

from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def edit_job(request, job_id):
    employer = get_object_or_404(Employer, user=request.user)
    job = get_object_or_404(Job, id=job_id, employer=employer)

    if request.method == "POST":
        designation = request.POST.get('designation', '').strip()
        description = request.POST.get('description', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        last_date = request.POST.get('last_date')
        job_type = request.POST.get('job_type')

        # ================= VALIDATIONS =================

        # Job designation
        if len(designation) < 3:
            messages.error(request, "Job designation must be at least 3 characters long.")
            return render(request, 'edit_job.html', {'job': job})

        # Job type
        if not job_type:
            messages.error(request, "Please select a job type.")
            return render(request, 'edit_job.html', {'job': job})

        # Job description
        if len(description) < 20:
            messages.error(
                request,
                "Job description must be at least 20 characters long."
            )
            return render(request, 'edit_job.html', {'job': job})

        # Job requirements
        if len(requirements) < 10:
            messages.error(
                request,
                "Job requirements must be at least 10 characters long."
            )
            return render(request, 'edit_job.html', {'job': job})

        # Last date validation
        try:
            last_date_obj = date.fromisoformat(last_date)
            if last_date_obj < date.today():
                messages.error(request, "Last date cannot be in the past.")
                return render(request, 'edit_job.html', {'job': job})
        except:
            messages.error(request, "Invalid last date.")
            return render(request, 'edit_job.html', {'job': job})

        # ================= UPDATE JOB =================
        job.designation = designation
        job.description = description
        job.requirements = requirements
        job.job_type = job_type
        job.last_date = last_date_obj
        job.save()

        messages.success(request, "Job updated successfully")
        return redirect('my_jobs')

    return render(request, 'edit_job.html', {'job': job})


def admin_jobs(request):
    jobs = Job.objects.filter(status=0)
    return render(request, 'admin_jobs.html', {'jobs': jobs})


def approve_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.status = 1
    job.save()

    notify_seekers_for_job(job)

    messages.success(request, "Job approved and seekers notified")
    return redirect('admin_jobs')



def reject_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()

    messages.success(request, 'Job rejected and deleted')
    return redirect('admin_jobs')

from datetime import timedelta
from django.utils.timezone import now

@login_required
def seeker_dashboard(request):
    seeker = Seeker.objects.get(user=request.user)

    # Profile completeness check
    profile_incomplete = not (
        seeker.education and seeker.resume
    )

    jobs = Job.objects.filter(status=1).order_by('-posted_date')

    # 🔍 FILTERS
    job_name = request.GET.get('job_name')
    job_type = request.GET.get('job_type')
    posted_time = request.GET.get('posted_time')
    location = request.GET.get('location')


    if job_name:
        jobs = jobs.filter(designation__icontains=job_name)
    if location:
        jobs = jobs.filter(
        employer__address__icontains=location
    )


    if job_type:
        jobs = jobs.filter(job_type=job_type)

    if posted_time == "today":
        jobs = jobs.filter(posted_date=now().date())

    elif posted_time == "7":
        jobs = jobs.filter(
            posted_date__gte=now().date() - timedelta(days=7)
        )

    elif posted_time == "30":
        jobs = jobs.filter(
            posted_date__gte=now().date() - timedelta(days=30)
        )

    return render(
        request,
        'seeker_dashboard.html',
        {
            'jobs': jobs,
            'profile_incomplete': profile_incomplete
        }
    )

from .models import Application

@login_required
def apply_job(request, job_id):
    seeker = Seeker.objects.get(user=request.user)
    job = Job.objects.get(id=job_id, status=1)

    if not seeker.education or not seeker.resume:
        messages.warning(
            request,
            "Complete your profile before applying for jobs."
        )
        return redirect('seeker_dashboard')

    if Application.objects.filter(seeker=seeker, job=job).exists(): 
        messages.info(request, "You have already applied for this job.")
        return redirect('seeker_dashboard')

    Application.objects.create(
        seeker=seeker,
        job=job
    )

    messages.success(request, "Job applied successfully!")
    return redirect('seeker_dashboard')


# 

@login_required
def seeker_profile(request):
    seeker = Seeker.objects.get(user=request.user)

    if request.method == "POST":
        # Existing Seeker fields
        seeker.education = request.POST.get('education')
        seeker.certifications = request.POST.get('certifications')
        seeker.address = request.POST.get('address')

        # ✅ FIXED: Mobile goes to Seeker.mobile (NOT CustomUser)
        new_mobile = request.POST.get('mobile')
        if new_mobile:
            # Indian mobile validation
            import re
            mobile_pattern = re.compile(r'^(?:(?:\+|0{0,2})91[\s\-]*|[0])?[6789]\d{9}$')
            if not mobile_pattern.match(new_mobile):
                messages.error(request, "Enter valid Indian mobile (e.g., 9876543210)")
                return redirect('seeker_profile')
            # Check duplicate mobile across ALL Seekers/Employers
            if Seeker.objects.filter(mobile=new_mobile).exclude(pk=seeker.pk).exists() or \
               Employer.objects.filter(mobile=new_mobile).exists():
                messages.error(request, "Mobile already registered")
                return redirect('seeker_profile')
            seeker.mobile = new_mobile

        # File uploads
        if request.FILES.get('profile_picture'):
            seeker.profile_picture = request.FILES.get('profile_picture')
        if request.FILES.get('resume'):
            seeker.resume = request.FILES.get('resume')

        # CustomUser fields (username, email)
        user = request.user
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_dob = request.POST.get('dob')

        # Username validation
        if new_username and new_username != user.username:
            if CustomUser.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, "Username already taken")
                seeker.save()
                return redirect('seeker_profile')
            user.username = new_username

        # STRICT Email validation
# STRICT Email validation (REPLACE your current email block)
        if new_email and new_email != user.email:
                try:
                    from django.core.validators import validate_email
                    validate_email(new_email)  # Django's built-in validator
        
        # ✅ CRITICAL: Check for REAL domains only
                    domain = new_email.split('@')[1].lower()
                    valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
                                     'rediffmail.com', 'yahoo.co.in', 'gmail.co.in']

                    if domain not in valid_domains:
                         messages.error(request, "Use valid email domains: gmail.com, yahoo.com, etc.")
                         seeker.save()
                         return redirect('seeker_profile')

                    if CustomUser.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                         messages.error(request, "Email already registered")
                         seeker.save()
                         return redirect('seeker_profile')

                    user.email = new_email
        
                except:
                        messages.error(request, "Invalid email format")
                        seeker.save()
                        return redirect('seeker_profile')


        # DOB update
        if new_dob:
            seeker.dob = new_dob

        user.save()
        seeker.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('seeker_profile')

    return render(request, 'seeker_profile.html', {'seeker': seeker})


@login_required
def applied_jobs(request):
    seeker = Seeker.objects.get(user=request.user)
    
    status_filter = request.GET.get('status')

    if status_filter:
        applications = Application.objects.filter(
            seeker=seeker,
            status=status_filter
        ).order_by('-applied_date')
    else:
        applications = Application.objects.filter(
            seeker=seeker
        ).order_by('-applied_date')

    # ✅ FIXED: Use underscore for spaces (template-friendly keys)
    status_counts = {
        'Applied': Application.objects.filter(seeker=seeker, status='Applied').count(),
        'Viewed': Application.objects.filter(seeker=seeker, status='Viewed').count(),
        'Profile_Visited': Application.objects.filter(seeker=seeker, status='Profile Visited').count(),
        'Accepted': Application.objects.filter(seeker=seeker, status='Accepted').count(),
        'Rejected': Application.objects.filter(seeker=seeker, status='Rejected').count(),
    }
    
    total_applications = sum(status_counts.values())

    return render(
        request,
        'applied_jobs.html',
        {
            'applications': applications,
            'status_filter': status_filter,
            'status_counts': status_counts,
            'total_applications': total_applications,
        }
    )


@login_required
def employer_jobs(request):
    jobs = Job.objects.filter(employer__user=request.user)

    return render(
        request,
        'employer_jobs.html',
        {'jobs': jobs}
    )


@login_required
def view_applicants(request, job_id):
    job = Job.objects.get(id=job_id, employer__user=request.user)
    applications = Application.objects.filter(job=job)

    return render(
        request,
        'view_applicants.html',
        {
            'job': job,
            'applications': applications
        }
    )


from .models import SeekerNotification


# from django.contrib import messages
# from django.shortcuts import render, redirect, get_object_or_404
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import Application, SeekerNotification

import uuid
from django.utils import timezone

# Add this helper function at top of views.py (before your view)
def trigger_profile_visited(application):
    """Auto trigger Profile Visited status + email/notification"""
    if application.status not in ["Profile Visited", "Accepted"]:
        seeker = application.seeker
        job = application.job
        seeker_email = seeker.user.email
        seeker_name = seeker.user.first_name or seeker.user.username
        
        # Update status
        application.status = "Profile Visited"
        application.save()
        
        # Notification
        msg = f"🎯 Employer visited your profile for {job.designation}"
        SeekerNotification.objects.create(seeker=seeker, message=msg)
        
        # Email
        if seeker_email:
            email_subject = "Your Profile Was Visited!"
            email_message = f"""
Hello {seeker_name},

🎯 Great news!

The employer at {job.employer.company_name} has visited your profile 
for the position "{job.designation}".

They are interested in your profile!

Regards,
Job Portal Team
"""
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [seeker_email],
                fail_silently=True
            )

@login_required
def update_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    
    # ✅ AUTO Profile Visited check (tracks if employer viewed profile recently)
    if request.GET.get('profile_viewed') == 'true':
        trigger_profile_visited(application)
        return redirect('view_applicants', application.job.id)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        
        # ✅ PERMANENT ACCEPTED STATUS LOGIC
        if application.status == "Accepted":
            messages.warning(request, "Cannot change status of already accepted applications")
            return redirect('view_applicants', application.job.id)
        
        # Update status
        application.status = new_status
        application.save()

        seeker = application.seeker
        job = application.job
        seeker_email = seeker.user.email
        seeker_name = seeker.user.first_name or seeker.user.username

        msg = None
        email_subject = None
        email_message = None

        if new_status == "Viewed":
            msg = f"Your application for {job.designation} was viewed."
            email_subject = "Your Job Application Was Viewed"
            email_message = f"""
Hello {seeker_name},

Your application for the position "{job.designation}"
at {job.employer.company_name} has been viewed by the employer.

They may contact you soon.

Regards,
Job Portal Team
"""

        elif new_status == "Profile Visited":
            msg = f"🎯 Employer visited your profile for {job.designation}"
            email_subject = "Your Profile Was Visited!"
            email_message = f"""
Hello {seeker_name},

🎯 Great news!

The employer at {job.employer.company_name} has visited your profile 
for the position "{job.designation}".

They are interested in your profile!

Regards,
Job Portal Team
"""

        elif new_status == "Accepted":
            msg = f"🎉 You have been selected for the job: {job.designation}"
            email_subject = "Congratulations! Application Accepted"
            email_message = f"""
Hello {seeker_name},

🎉 Congratulations!

Your application for the position "{job.designation}"
at {job.employer.company_name} has been **ACCEPTED**.

Please login to your account for further updates.

Regards,
Job Portal Team
"""

        elif new_status == "Rejected":
            msg = f"Your application for {job.designation} was rejected."
            email_subject = "Job Application Update"
            email_message = f"""
Hello {seeker_name},

Thank you for applying for "{job.designation}"
at {job.employer.company_name}.

Unfortunately, your application was not selected this time.
We encourage you to apply for other jobs.

Regards,
Job Portal Team
"""

        if msg:
            SeekerNotification.objects.create(
                seeker=seeker,
                message=msg
            )

        if email_subject and seeker_email:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [seeker_email],
                fail_silently=True
            )

        messages.success(request, f"Status updated to '{new_status}' and notification sent")
        return redirect('view_applicants', job.id)
    
    return redirect('view_applicants', application.job.id)

from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def seeker_profile_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    seeker = get_object_or_404(Seeker, user=user)
    
    # ✅ AUTO Profile Visited + CAPTURE JOB
    job = None
    if request.GET.get('app_id'):
        try:
            app_id = int(request.GET.get('app_id'))
            application = Application.objects.get(id=app_id, seeker=seeker)
            trigger_profile_visited(application)
            job = application.job  # ✅ PASS JOB BACK
        except (Application.DoesNotExist, ValueError):
            pass
    
    return render(request, 'employer_seeker_detail.html', {
        'seeker': seeker,
        'user': user,
        'job': job  # ✅ FIXED: Pass job for back button
    })


@login_required
def employer_notifications(request):
    jobs = Job.objects.filter(employer__user=request.user)

    notifications = Application.objects.filter(
        job__in=jobs,
        status='Applied'
    ).order_by('-applied_date')

    return render(
        request,
        'employer_notifications.html',
        {'notifications': notifications}
    )





@login_required
def employer_account(request):
    employer = Employer.objects.get(user=request.user)
    user = request.user

    if request.method == "POST":
        form_type = request.POST.get('form_type')

        # ================= PROFILE UPDATE =================
        if form_type == "profile":
            company_name = request.POST.get('company_name', '').strip()
            fname = request.POST.get('first_name', '').strip()
            lname = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            mobile = request.POST.get('mobile', '').strip()
            address = request.POST.get('address', '').strip()

            # 🔴 Name validation (existing)
            if len(company_name) < 3:
                messages.error(request, "Company name must be at least 3 characters.")
                return redirect('employer_account')
            if len(fname) < 3 or not re.fullmatch(r'[A-Za-z ]+', fname):
                messages.error(request,"First name must be at least 3 characters and contain only letters")
                return redirect('employer_account')
            if lname and not re.fullmatch(r'[A-Za-z ]+', lname):
                messages.error(request,"Last name must contain only letters")
                return redirect('employer_account')

            # ✅ FIXED: STRICT EMAIL VALIDATION + DOMAIN WHITELIST
            if email != user.email:
                try:
                    from django.core.validators import validate_email
                    validate_email(email)
                    
                    # ✅ DOMAIN WHITELIST (blocks abc@gm.com)
                    domain = email.split('@')[1].lower()
                    valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
                                   'rediffmail.com', 'yahoo.co.in', 'gmail.co.in']
                    
                    if domain not in valid_domains:
                        messages.error(request, "Use valid domains: gmail.com, yahoo.com, etc.")
                        return redirect('employer_account')
                        
                    if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
                        messages.error(request, "Email already registered")
                        return redirect('employer_account')
                        
                except:
                    messages.error(request, "Invalid email format")
                    return redirect('employer_account')

            # ✅ STRICT MOBILE VALIDATION (same as seeker_profile)
            if mobile != employer.mobile:
                mobile_pattern = re.compile(r'^(?:(?:\+|0{0,2})91[\s\-]*|[0])?[6789]\d{9}$')
                if not mobile_pattern.match(mobile):
                    messages.error(request, "Enter valid Indian mobile (e.g., 9876543210 or +919876543210)")
                    return redirect('employer_account')
                
                # Check duplicates across ALL Employers + Seekers
                if Employer.objects.filter(mobile=mobile).exclude(pk=employer.pk).exists() or \
                   Seeker.objects.filter(mobile=mobile).exists():
                    messages.error(request, "Mobile number already registered")
                    return redirect('employer_account')

            # 🔴 Address validation
            if len(address) < 3:
                messages.error(request, "Address must be at least 10 characters long")
                return redirect('employer_account')

            # ✅ SAVE PROFILE
            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()

            employer.company_name = company_name
            employer.mobile = mobile
            employer.address = address
            employer.save()

            messages.success(request, "Profile updated successfully")
            return redirect('employer_account')

        # ================= WEBSITE UPDATE =================
        elif form_type == "website":
            employer.website = request.POST.get('website')
            employer.save()
            messages.success(request, "Website updated successfully")
            return redirect('employer_account')

        # ================= PASSWORD UPDATE =================
        elif form_type == "password":
            current = request.POST.get('current_password')
            new = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')

            if not user.check_password(current):
                messages.error(request, "Current password is incorrect")
                return redirect('employer_account')

            if new != confirm:
                messages.error(request, "Passwords do not match")
                return redirect('employer_account')

            if (
                len(new) < 6 or
                not re.search(r'[A-Z]', new) or
                not re.search(r'[0-9]', new) or
                not re.search(r'[!@#$%^&*(),.?":{}|<>]', new)
            ):
                messages.error(
                    request,
                    "Password must contain uppercase, number & special character"
                )
                return redirect('employer_account')

            user.set_password(new)
            user.save()
            messages.success(request, "Password updated successfully. Please login again.")
            return redirect('login_view')

    return render(request, 'employer_account.html', {'employer': employer})

@login_required
def admin_account(request):
    user = request.user   # ✅ CORRECT

    if request.method == "POST":

        # 🔹 EMAIL UPDATE
        if 'email' in request.POST:
            email = request.POST.get('email', '').strip()

            # ✅ FIXED: STRICT EMAIL VALIDATION + DOMAIN WHITELIST
            try:
                from django.core.validators import validate_email
                validate_email(email)
                
                # ✅ DOMAIN WHITELIST (blocks abc@gm.com)
                domain = email.split('@')[1].lower()
                valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 
                               'rediffmail.com', 'yahoo.co.in', 'gmail.co.in']
                
                if domain not in valid_domains:
                    messages.error(request, "Use valid domains: gmail.com, yahoo.com, etc.")
                    return redirect('admin_account')
                    
            except:
                messages.error(request, "Invalid email format")
                return redirect('admin_account')

            if email != user.email:
                user.email = email
                user.save()
                messages.success(request, "Email updated successfully")
            else:
                messages.info(request, "Email is unchanged")

        # 🔹 PASSWORD UPDATE
        elif 'current_password' in request.POST:
            current = request.POST.get('current_password')
            new = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')

            if not check_password(current, user.password):
                messages.error(request, "Current password is incorrect")

            elif new != confirm:
                messages.error(request, "Passwords do not match")

            elif (
                len(new) < 6
                or not re.search(r'[A-Z]', new)
                or not re.search(r'\d', new)
                or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new)
            ):
                messages.error(
                    request,
                    "Password must contain uppercase, number & special character"
                )
            else:
                user.set_password(new)
                user.save()
                messages.success(
                    request,
                    "Password updated successfully. Please re-login"
                )
                return redirect('login_view')

    return render(request, 'admin_account.html')


@login_required
def admin_notifications(request):

    pending_users = CustomUser.objects.filter(
        status=0
    ).exclude(user_type="1")

    pending_jobs = Job.objects.filter(status=0)
    new_applications = Application.objects.filter(status='Applied')

    # ✅ STEP 3: MARK AS SEEN
    Job.objects.filter(status=0, admin_seen=False).update(admin_seen=True)
    Application.objects.filter(
        status='Applied',
        admin_seen=False
    ).update(admin_seen=True)

    return render(
        request,
        'admin_notifications.html',
        {
            'pending_users': pending_users,
            'pending_jobs': pending_jobs,
            'new_applications': new_applications
        }
    )


@login_required
def admin_view_jobs(request):
    jobs = Job.objects.all().order_by('-posted_date')
    return render(request, 'admin_view_jobs.html', {'jobs': jobs})

from django.contrib.auth import update_session_auth_hash

@login_required
def seeker_change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        # Check current password
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('seeker_profile')

        # Match check
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('seeker_profile')

        # Password validation
        if (
            len(new_password) < 6 or
            not re.search(r'[A-Z]', new_password) or
            not re.search(r'\d', new_password) or
            not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password)
        ):
            messages.error(
                request,
                "Password must contain at least 6 characters, "
                "1 uppercase letter, 1 number and 1 special character."
            )
            return redirect('seeker_profile')

        # Save password
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully.Please Re-login")
        return redirect('login_view')
    


@login_required
def verify_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    user.is_verified = True
    user.save()

    messages.success(request, f"{user.username} has been verified.")
    return redirect(request.META.get('HTTP_REFERER', 'admindash'))


@login_required
def unverify_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    user.is_verified = False
    user.save()

    messages.warning(request, f"{user.username} verification removed.")
    return redirect(request.META.get('HTTP_REFERER', 'admindash'))





@login_required
def seeker_notifications(request):
    seeker = Seeker.objects.get(user=request.user)

    notifications = SeekerNotification.objects.filter(
        seeker=seeker
    ).order_by('-created_at')

    # ✅ MARK ALL AS READ WHEN VIEWED
    notifications.filter(is_read=False).update(is_read=True)

    return render(
        request,
        'seeker_notifications.html',
        {'notifications': notifications}
    )





def notify_seekers_for_job(job):
    preferences = SeekerNotificationPreference.objects.all()

    for pref in preferences:
        company_match = False
        title_match = False

        if pref.preferred_company:
            company_match = pref.preferred_company.lower() in job.employer.company_name.lower()

        if pref.preferred_title:
            title_match = pref.preferred_title.lower() in job.designation.lower()

        if company_match or title_match:
            send_mail(
                subject="New Job Alert – Job Portal",
                message=(
                    f"Hello {pref.seeker.user.first_name},\n\n"
                    f"A new job matching your preferences has been posted.\n\n"
                    f"Job Title: {job.designation}\n"
                    f"Company: {job.employer.company_name}\n"
                    f"Last Date: {job.last_date}\n\n"
                    f"Login to Job Portal to apply."
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[pref.seeker.user.email],
                fail_silently=True
            )


@login_required
def seeker_notification_settings(request):
    seeker = Seeker.objects.get(user=request.user)

    preference, created = SeekerNotificationPreference.objects.get_or_create(
        seeker=seeker
    )

    if request.method == "POST":
        preference.preferred_company = request.POST.get('preferred_company', '')
        preference.preferred_title = request.POST.get('preferred_title', '')
        preference.save()

        messages.success(request, "Notification preferences updated")
        return redirect('seeker_notification_settings')

    return render(
        request,
        'seeker_notification_settings.html',
        {'preference': preference}
    )
