from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('alumni-dashboard/', views.alumni_dashboard, name='alumni_dashboard'),
    path("admin/alumni/", views.admin_view_alumni, name="admin_view_alumni"),
    path("event/create/", views.create_event, name="create_event"),
    path("admin-portal/", views.admin_portal, name="admin_portal"),
    path("alumni-portal/", views.alumni_portal, name="alumni_portal"),
    path('alumni/feedback/', views.alumni_feedback, name='alumni_feedback'),
    path('admin/feedback/', views.admin_feedback, name='admin_feedback'),
    # path("admin/events/", views.admin_events, name="admin_events"),
    # path("admin/events/approve/<int:id>/", views.approve_event, name="approve_event"),
    # path("admin/events/reject/<int:id>/", views.reject_event, name="reject_event"),
    # path("admin/events/", views.manage_admin_events, name="admin_events"),
    # path("admin/alumni/", views.view_alumni, name="view_alumni"),
    path("admin/announcements/", views.admin_announcements, name="admin_announcements"),
    path("admin/announcements/add/", views.add_announcement, name="add_announcement"),
    path("admin/announcements/edit/<int:id>/", views.edit_announcement, name="edit_announcement"),
    path("admin/announcements/delete/<int:id>/", views.delete_announcement, name="delete_announcement"),
    path('announcements/', views.alumni_announcements, name='alumni_announcements'),
    path("admin/events/manage/", views.manage_admin_events, name="admin_events"),
    path("admin/events/", views.view_events_admin, name="view_events_admin"),
    # path("admin/events/", views.view_events_admin, name="view_events_admin"),
    path("alumni/events/", views.view_events_alumni, name="view_events_alumni"),
    path("events/manage/", views.manage_events, name="manage_events"),
    path('events/edit/<int:id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:id>/', views.delete_event, name='delete_event'),
    # JOBS
    # ===== ALUMNI JOBS =====
    path("alumni/jobs/manage/", views.manage_jobs_alumni, name="manage_jobs_alumni"),
    path("alumni/jobs/", views.view_jobs_alumni, name="view_jobs_alumni"),
    # ===== ALUMNI JOB ACTIONS =====
    path("alumni/jobs/add/", views.add_job_alumni, name="add_job_alumni"),
    path("alumni/jobs/edit/<int:id>/", views.edit_job_alumni, name="edit_job_alumni"),
    path("alumni/jobs/delete/<int:id>/", views.delete_job_alumni, name="delete_job_alumni"),
    # ===== ADMIN JOBS =====
    path("admin/jobs/manage/", views.manage_jobs_admin, name="manage_jobs_admin"),
    path("admin/jobs/", views.view_jobs_admin, name="view_jobs_admin"),
    # ===== ADMIN JOB ACTIONS =====
    path("admin/jobs/add/", views.add_job_admin, name="add_job_admin"),
    path("admin/jobs/edit/<int:id>/", views.edit_job_admin, name="edit_job_admin"),
    path("admin/jobs/delete/<int:id>/", views.delete_job_admin, name="delete_job_admin"),

]