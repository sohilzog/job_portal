from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admindash', views.admindash, name='admindash'),
path('admin_account',views.admin_account,name='admin_account'),
path('admin_notifications', views.admin_notifications, name='admin_notifications'),
path('admin_view_jobs', views.admin_view_jobs, name='admin_view_jobs'),



    path('employerdash', views.employerdash, name='employerdash'),



    # 🔐 Authentication
    path('login_view', views.login_view, name='login_view'),
    path('logout_view', views.logout_view, name='logout_view'),

    
    path('seeker_reg', views.seeker_reg, name='seeker_reg'),
    path('seeker_change_password', views.seeker_change_password, name='seeker_change_password'),
    path('seeker_notifications', views.seeker_notifications, name='seeker_notifications'),
    path('seeker_notification_settings', views.seeker_notification_settings, name='seeker_notification_settings'),
    path('seeker/profile/<int:user_id>/', views.seeker_profile_detail, name='seeker_profile_detail'),




    path('employer_reg', views.employer_reg, name='employer_reg'),

    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('unverify_user/<int:user_id>/', views.unverify_user, name='unverify_user'),

    path('approve_disapprove', views.approve_disapprove, name='approve_disapprove'),
    path('approve/<int:k>/', views.approve, name='approve'),
    path('disapprove/<int:k>/', views.disapprove, name='disapprove'),

    path('view_employers', views.view_employers, name='view_employers'),
    path('view_seekers', views.view_seekers, name='view_seekers'),

    path('post_job', views.post_job, name='post_job'),
    path('my_jobs', views.my_jobs, name='my_jobs'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>/', views.delete_job, name='delete_job'),


    path('admin_jobs', views.admin_jobs, name='admin_jobs'),
    path('approve_job/<int:job_id>/', views.approve_job, name='approve_job'),
    path('reject_job/<int:job_id>/', views.reject_job, name='reject_job'),

    path('seeker_dashboard', views.seeker_dashboard, name='seeker_dashboard'),
    path('apply_job/<int:job_id>/', views.apply_job, name='apply_job'),
     path('seeker_profile', views.seeker_profile, name='seeker_profile'),
     path('applied_jobs', views.applied_jobs, name='applied_jobs'),




    # Employer
path('employer/jobs/', views.employer_jobs, name='employer_jobs'),
path('employer/job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
path('employer/application/<int:app_id>/update/', views.update_application_status, name='update_application_status'),
path('employer_notifications',views.employer_notifications,name='employer_notifications'),
path('employer_account',views.employer_account,name='employer_account'),




path('delete_employer/<int:user_id>/', views.delete_employer, name='delete_employer'),
path('delete_seeker/<int:user_id>/', views.delete_seeker, name='delete_seeker'),




]
