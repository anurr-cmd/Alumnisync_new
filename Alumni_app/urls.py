from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.login_portal, name='login_portal'),
    path('logout/', views.logout_view, name='logout'),

    # Alumini
    path("register/alumni/", views.alumni_register, name="alumni_register"),
    path('alumni/login/', views.alumni_login, name='alumni_login'),
    path('alumni-dashboard/', views.alumni_dashboard, name='alumni_dashboard'),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path('alumni/feedback/', views.alumni_feedback, name='alumni_feedback'),

    # Admin
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    
    
    path("admin/alumni/", views.admin_view_alumni, name="admin_view_alumni"),
    path("admin/alumni/add/", views.admin_add_alumni, name="admin_add_alumni" ),
    path("admin/alumni/edit/<int:pk>/", views.admin_edit_alumni, name="admin_edit_alumni"),
    path("admin/alumni/user/<int:pk>/", views.admin_view_user, name="admin_view_user" ),
    
    path(
    "admin/user/<int:pk>/",
    views.admin_view_user,
    name="admin_view_user"
),
    
    path('admin/feedback/', views.admin_feedback, name='admin_feedback'),    
    path("admin/events/", views.manage_admin_events, name="admin_events"),
    
    path("admin/announcements/", views.admin_announcements, name="admin_announcements"),
    path("admin/announcements/add/", views.add_announcement, name="add_announcement"),
    path("admin/announcements/edit/<int:id>/", views.edit_announcement, name="edit_announcement"),
    path("admin/announcements/delete/<int:id>/", views.delete_announcement, name="delete_announcement"),
    
    path('announcements/', views.alumni_announcements, name='alumni_announcements'),
    path("events/create/", views.create_event, name="create_event"),
    path('edit-event/<int:id>/', views.edit_event, name='edit_event'),
    path("events/delete/<int:id>/", views.delete_event, name="delete_event"),
    
    path("alumni/jobs/manage/", views.jobs_alumni, name="jobs_alumni"),
    path("admin/jobs/",views.jobs_admin,name="jobs_admin"),
    path("alumni/jobs/add/", views.add_job_alumni, name="add_job_alumni"),
    path("edit-job-alumni/<int:id>/", views.edit_job_alumni, name="edit_job_alumni"),
    path("alumni/jobs/delete/<int:id>/", views.delete_job_alumni, name="delete_job_alumni"),
]