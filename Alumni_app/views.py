import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Profile,Event,Job,Announcement
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.db import IntegrityError
from .models import Feedback

logger = logging.getLogger(__name__)

def index(request):

    alumni_count = Profile.objects.filter(role="alumni").count()
    event_count = Event.objects.count()
    job_count = Job.objects.count()
    announcement_count = Announcement.objects.count()

    context = {
        "alumni_count": alumni_count,
        "event_count": event_count,
        "job_count": job_count,
        "announcement_count": announcement_count,
    }

    return render(request, "index.html", context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_portal(request):
    return render(request, 'login_portal.html')

def alumni_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                profile = Profile.objects.get(user=user)

                if profile.role == "alumni":
                    login(request, user)
                    return redirect("alumni_dashboard")
                else:
                    messages.error(request, "You are not an Alumni user.")

            except Profile.DoesNotExist:
                messages.error(request, "Profile not found.")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "alumni_login.html")

def admin_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_superuser:
                login(request, user)
                return redirect("admin_dashboard")

            try:
                profile = Profile.objects.get(user=user)

                if profile.role == "admin":
                    login(request, user)
                    return redirect("admin_dashboard")
                else:
                    messages.error(request, "You are not an Admin user.")

            except Profile.DoesNotExist:
                messages.error(request, "Profile not found.")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "admin_login.html")
# def forgot_password(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         new_password = request.POST.get("new_password")
#         confirm_password = request.POST.get("confirm_password")

#         if new_password != confirm_password:
#             return render(request, "login.html", {"error": "Passwords do not match."})

#         try:
#             user = User.objects.get(username=username)
#             user.set_password(new_password)  # securely update password
#             user.save()
#             return render(request, "login.html", {"message": "Password reset successful! You can now login."})
#         except User.DoesNotExist:
#             return render(request, "login.html", {"error": "Username not found."})

#     return redirect("login_view")



def logout_view(request):
    logout(request)
    return redirect("login_portal")

def alumni_register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("alumni_dashboard")

    return render(request,"alumni_register.html")

@login_required
def alumni_dashboard(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        "profile": profile,

        "total_events": Event.objects.count(),
        "total_jobs": Job.objects.count(),
        "total_announcements": Announcement.objects.count(),

        "recent_events": Event.objects.order_by("-date")[:3],
        "recent_jobs": Job.objects.order_by("-posted_on")[:3],
        "recent_announcements": Announcement.objects.order_by("-posted_on")[:3],
    }

    return render(request, "alumni_dashboard.html", context)

@login_required
def edit_profile(request):
    profile = request.user.profile  # assuming OneToOneField

    if request.method == "POST":
        # Text fields
        profile.roll_no = request.POST.get("roll_no")
        profile.email = request.POST.get("email")
        profile.designation = request.POST.get("designation") or None
        profile.appointment_order = request.POST.get("appointment_order")
        profile.remarks = request.POST.get("remarks") or None
        profile.department = request.POST.get("department")
        profile.address = request.POST.get("address") or None
        profile.current_job = request.POST.get("current_job")
        profile.company = request.POST.get("company")
        profile.location = request.POST.get("location")
        profile.phone = request.POST.get("phone")
        profile.alternate_phone = request.POST.get("alternate_phone")

        # Integer fields
        join_year = request.POST.get("join_year")
        if join_year and join_year != "None":
            profile.join_year = int(join_year)
        else:
            profile.join_year = None


        passout_year = request.POST.get("passout_year")
        if passout_year and passout_year != "None":
            profile.passout_year = int(passout_year)
        else:
            profile.passout_year = None
        # File fields
        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        if request.FILES.get("proof_id"):
            profile.proof_id = request.FILES.get("proof_id")

        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("alumni_dashboard")

    return redirect("alumni_dashboard")

def superuser_required(user):
    return user.is_superuser

def admin_dashboard(request):

    total_alumni = Profile.objects.filter(role="alumni").count()
    total_events = Event.objects.count()
    total_jobs = Job.objects.count()
    total_announcements = Announcement.objects.count()

    recent_events = Event.objects.order_by('-date')[:5]
    recent_jobs = Job.objects.order_by('-posted_on')[:5]

    return render(request,"admin_dashboard.html",{
        "total_alumni": total_alumni,
        "total_events": total_events,
        "total_jobs": total_jobs,
        "total_announcements": total_announcements,
        "recent_events": recent_events,
        "recent_jobs": recent_jobs
    })

# @login_required
# def alumni_dashboard(request):
#     return render(request, "alumni_dashboard.html")


def admin_view_alumni(request):
    q = request.GET.get('q', '')
    logger.info(f"Search query: {q}")

    profiles = Profile.objects.select_related('user').all()

    if q:
        # Check if query is a year
        try:
            year = int(q)
            year_filter = Q(join_year=year) | Q(passout_year=year)
        except ValueError:
            year_filter = Q(join_year__icontains=q) | Q(passout_year__icontains=q)

        # Apply search filters
        profiles = profiles.filter(
            Q(user__username__icontains=q) |
            Q(roll_no__icontains=q) |
            Q(email__icontains=q) |
            Q(department__icontains=q) |
            Q(current_job__icontains=q) |
            Q(company__icontains=q) |
            Q(location__icontains=q) |
            Q(phone__icontains=q) |
            Q(alternate_phone__icontains=q) |
            Q(designation__icontains=q) |
            year_filter
        ).distinct()

    # If AJAX request return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []

        for p in profiles:
            data.append({
                "username": p.user.username if p.user else "",
                "roll_no": p.roll_no or "",
                "email": p.email or "",
                "department": p.department or "",
                "join_year": p.join_year or "",
                "passout_year": p.passout_year or "",
                "current_job": p.current_job or "",
                "company": p.company or "",
                "location": p.location or "",
                "phone": p.phone or "",
                "designation": p.designation or ""
            })

        return JsonResponse({"profiles": data})

    return render(request, "admin_view_alumni.html", {
        "profiles": profiles,
        "query": q
    })

# @login_required
# def alumni_portal(request):
#     job_count = Job.objects.count()
#     event_count = Event.objects.count()
#     announcement_count = Announcement.objects.count()

#     return render(request, "alumni_portal.html", {
#         "job_count": job_count,
#         "event_count": event_count,
#         "announcement_count": announcement_count,
#     })

@login_required
def admin_portal(request):
    job_count = Job.objects.count()

    return render(request, "admin_portal.html", {
        "job_count": job_count
    })



@login_required
def create_event(request):

    if request.method == "POST":

        Event.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            date=request.POST["date"],
            created_by=request.user
        )

        messages.success(request, "Event submitted for admin approval")

        return redirect("create_event")

    # GET request
    events = Event.objects.filter(is_approved=True).order_by("-date")

    return render(request, "create_event.html", {
        "events": events
    })

# @login_required
# def view_events_admin(request):
#     events = Event.objects.filter(is_approved=True)
#     return render(request, "view_events_admin.html", {"events": events})


# @login_required
# def view_events_alumni(request):
#     events = Event.objects.filter(is_approved=True)
#     return render(request, "view_events_alumni.html", {"events": events})


# 🔹 MANAGE EVENTS (Main Page)
# @login_required
# def manage_events(request):

#     if request.method == "POST":

#         Event.objects.create(
#             title=request.POST["title"],
#             description=request.POST["description"],
#             date=request.POST["date"],
#             created_by=request.user
#         )

#         return redirect("manage_events")

#     events = Event.objects.filter(is_approved=True).order_by("-date")

#     return render(request, "manage_events.html", {
#         "events": events
#     })

# 🔹 EDIT EVENT (Modal form submits here)
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.date = request.POST.get("date")
        event.save()

    return redirect("create_event")


# 🔹 DELETE EVENT
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('create_event')

# ===== ANNOUNCEMENTS =====
def announcements_page(request):

    announcements = Announcement.objects.all().order_by('-posted_on')

    context = {
        'announcements': announcements
    }

    return render(request, 'admin_announcements.html', context)



# ADD ANNOUNCEMENT
def add_announcement(request):

    if request.method == "POST":

        title = request.POST.get('title')
        message = request.POST.get('message')
        image_url = request.POST.get('image_url')

        Announcement.objects.create(
            title=title,
            message=message,
            image_url=image_url
        )

    return redirect('announcements_page')



# EDIT ANNOUNCEMENT
def edit_announcement(request, id):

    announcement = get_object_or_404(Announcement, id=id)

    if request.method == "POST":

        announcement.title = request.POST.get('title')
        announcement.message = request.POST.get('message')

        announcement.save()

    return redirect('announcements_page')



# DELETE ANNOUNCEMENT
def delete_announcement(request, id):

    announcement = get_object_or_404(Announcement, id=id)

    announcement.delete()

    return redirect('announcements_page')

# -----jobs----

# @login_required
# def view_jobs_alumni(request):
#     jobs = Job.objects.all().order_by("-posted_on")

#     return render(request, "view_jobs_alumni.html", {
#         "jobs": jobs
#     })

@login_required
def view_jobs_admin(request):
    jobs = Job.objects.order_by("-posted_on")

    return render(request, "view_jobs_admin.html", {
        "jobs": jobs
    })


@login_required
def jobs_alumni(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "alumni":
        return redirect("index")   # ✅ change here

    if request.method == "POST":
        Job.objects.create(
            title=request.POST["title"],
            company=request.POST["company"],
            description=request.POST["description"],
            # location=request.POST["location"],
            posted_by=request.user
        )
        return redirect("jobs_alumni")

    jobs = Job.objects.all().order_by("-posted_on")

    return render(request, "jobs_alumni.html", {"jobs": jobs})

@login_required
def jobs_admin(request):
    profile = Profile.objects.get(user=request.user)

    # Only admin allowed here
    if profile.role.lower() != "admin":
        return redirect("jobs_admin")

    if request.method == "POST":
        job = get_object_or_404(Job, id=request.POST["job_id"])
        action = request.POST["action"]

        if action == "approve":
            job.is_approved = True
        elif action == "reject":
            job.is_approved = False

        job.save()
        return redirect("jobs_admin")

    jobs = Job.objects.all()

    return render(request, "jobs_admin.html", {
        "jobs": jobs,
        "portal": "admin"
    })


@login_required
def add_job_alumni(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "alumni":
        return redirect("manage_jobs_alumni")

    if request.method == "POST":
        Job.objects.create(
        title=request.POST.get("title"),
        company=request.POST.get("company"),
        description=request.POST.get("description"),
        # location=request.POST.get("location"),
        posted_by=request.user
)

    return redirect("jobs_alumni")

@login_required
def add_job(request):

    if request.method == "POST":

        title = request.POST.get("title")
        company = request.POST.get("company")
        description = request.POST.get("description")

        Job.objects.create(
            title=title,
            company=company,
            description=description,
            posted_by=request.user
        )

        return redirect("jobs_admin")


@login_required
def edit_job_alumni(request, id):
    job = get_object_or_404(Job, id=id)
    profile = Profile.objects.get(user=request.user)

    # Alumni can edit ONLY their jobs
    if profile.role.lower() == "alumni" and job.posted_by != request.user:
        return redirect("jobs_alumni")

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.company = request.POST.get("company")
        job.description = request.POST.get("description")
        # job.location = request.POST.get("location")
        job.save()

    return redirect("jobs_alumni")

@login_required
def edit_job(request,id):

    job = Job.objects.get(id=id)

    if request.method == "POST":

        job.title = request.POST.get("title")
        job.company = request.POST.get("company")
        job.description = request.POST.get("description")

        job.save()

        return redirect("jobs_admin")


@login_required
def delete_job_alumni(request, id):
    job = get_object_or_404(Job, id=id)

    if job.posted_by != request.user:
        return redirect("jobs_alumni")

    job.delete()
    return redirect("jobs_alumni")

@login_required
def delete_job(request,id):

    job = Job.objects.get(id=id)

    job.delete()

    return redirect("admin_jobs")

@login_required
def view_alumni(request):
    alumni = Profile.objects.filter(role="alumni")
    return render(request, "admin_view_alumni.html", {"alumni": alumni})

@login_required
def admin_announcements(request):
    announcements = Announcement.objects.all()
    return render(request, "admin_announcements.html", {"announcements": announcements})

def is_admin(user):
    return user.is_staff
    
def alumni_announcements(request):
    announcements = Announcement.objects.all().order_by('-posted_on')
    return render(request, 'alumni_announcements.html', {
        'announcements': announcements
    })

@login_required
def manage_admin_events(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "admin":
        return redirect("login_portal")

    events = Event.objects.all().order_by("-id")

    if request.method == "POST":

        event_id = request.POST.get("event_id")
        action = request.POST.get("action")

        event = get_object_or_404(Event, id=event_id)

        # ✅ APPROVE
        if action == "approve":
            event.is_approved = True
            event.is_rejected = False
            event.save()

        # ❌ REJECT
        elif action == "reject":
            event.is_rejected = True
            event.is_approved = False
            event.save()

        # ✏️ EDIT
        elif action == "edit":
            event.title = request.POST.get("title")
            event.description = request.POST.get("description")
            event.date = request.POST.get("date")
            event.location = request.POST.get("location")
            event.save()

        # 🗑 DELETE
        elif action == "delete":
            event.delete()

        return redirect("admin_events")

    return render(request, "admin_events.html", {"events": events})

def alumni_feedback(request):

    if request.method == "POST":

        message = request.POST.get("message")
        name = request.POST.get("name")

        if request.user.is_authenticated:

            Feedback.objects.create(
                user=request.user,
                message=message
            )

        else:

            Feedback.objects.create(
                name=name,
                message=message
            )

        return redirect("alumni_feedback")

    feedbacks = Feedback.objects.all().order_by("-created_at")

    return render(request, "alumni_feedback.html", {"feedbacks": feedbacks})


@login_required
def admin_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, "admin_feedback.html", {"feedbacks": feedbacks})

