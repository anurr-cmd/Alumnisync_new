from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Profile,Event,Job,Announcement
from .forms import EventForm

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   # creates session

            # 🔑 role-based redirect
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found. Contact admin.")
                return redirect("login")

            # Respect ?next= first (for protected pages)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            if profile.role == "admin":
                return redirect("admin_dashboard")
            elif profile.role == "alumni":
                return redirect("alumni_dashboard")
            else:
                return redirect("login")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(request, "login.html", {"error": "Passwords do not match."})

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)  # securely update password
            user.save()
            return render(request, "login.html", {"message": "Password reset successful! You can now login."})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Username not found."})

    return redirect("login_view")



def logout_view(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role") or "alumni"

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)

        passout_year = request.POST.get("passout_year")
        passout_year = int(passout_year) if passout_year else None
        profile_image = request.FILES.get("profile_image")
        Profile.objects.create(
            user=user,
            role=role,
            profile_image=profile_image, 
            roll_no=request.POST.get("roll_no"),
            department=request.POST.get("department"),
            passout_year=passout_year,
            current_status=request.POST.get("current_status"),
            company=request.POST.get("company"),
            location=request.POST.get("location"),
            phone=request.POST.get("phone"),
        )

        login(request, user)  # 🔑 auto login after register

        if role == "admin":
            return redirect("admin_portal")
        return redirect("alumni_portal")

    return render(request, "register.html")


@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@login_required
def alumni_dashboard(request):
    return render(request, "alumni_dashboard.html")


@login_required
def admin_view_alumni(request):

    # Ensure admin profile exists
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "Admin"}
    )

    # Force admin role for admin section
    if profile.role.lower() != "admin":
        profile.role = "Admin"
        profile.save()

    # Fetch alumni (case-insensitive)
    alumni_list = Profile.objects.filter(role__iexact="alumni")

    return render(request, "admin_view_alumni.html", {
        "alumni_list": alumni_list
    })

@login_required
def alumni_portal(request):
    job_count = Job.objects.count()
    event_count = Event.objects.count()
    announcement_count = Announcement.objects.count()

    return render(request, "alumni_portal.html", {
        "job_count": job_count,
        "event_count": event_count,
        "announcement_count": announcement_count,
    })

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
        return redirect("alumni_portal")

    return render(request, "create_event.html")

@login_required
def view_events_admin(request):
    events = Event.objects.filter(is_approved=True)
    return render(request, "view_events_admin.html", {"events": events})


@login_required
def view_events_alumni(request):
    events = Event.objects.filter(is_approved=True)
    return render(request, "view_events_alumni.html", {"events": events})


# 🔹 MANAGE EVENTS (Main Page)
def manage_events(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'manage_events.html', {'events': events})


# 🔹 EDIT EVENT (Modal form submits here)
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.date = request.POST.get('date')
        event.save()

    return redirect('manage_events')


# 🔹 DELETE EVENT
def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('manage_events')

# ===== ANNOUNCEMENTS =====
def announcements(request):
    announcements = Announcement.objects.all()
    return render(request, "announcements.html", {"announcements": announcements})

@login_required
def add_announcement(request):
    if request.method == "POST":
        Announcement.objects.create(
            title=request.POST["title"],
            message=request.POST["message"],
            image_url=request.POST.get('image_url', '')
        )
    return redirect("admin_announcements")



@login_required
def edit_announcement(request, id):
    announcement = Announcement.objects.get(id=id)

    if request.method == "POST":
        announcement.title = request.POST['title']
        announcement.message = request.POST['message']
        announcement.image_url = request.POST.get('image_url', '')
        announcement.save()

    return redirect('admin_announcements')

@login_required
def delete_announcement(request, id):
    ann = get_object_or_404(Announcement, id=id)
    ann.delete()
    return redirect("admin_announcements")

# -----jobs----

@login_required
def view_jobs_alumni(request):
    jobs = Job.objects.all().order_by("-posted_on")

    return render(request, "view_jobs_alumni.html", {
        "jobs": jobs
    })

@login_required
def view_jobs_admin(request):
    jobs = Job.objects.order_by("-posted_on")

    return render(request, "view_jobs_admin.html", {
        "jobs": jobs
    })


@login_required
def manage_jobs_alumni(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "alumni":
        return redirect("manage_jobs_alumni")

    if request.method == "POST":
        Job.objects.create(
            title=request.POST["title"],
            company=request.POST["company"],
            description=request.POST["description"],
            location=request.POST["location"],
            posted_by=request.user   # ✅ FIXED
        )
        return redirect("manage_jobs_alumni")

    jobs = Job.objects.filter(posted_by=request.user)  # ✅ FIXED

    return render(request, "manage_jobs_alumni.html", {
        "jobs": jobs,
        "portal": "alumni"
    })

@login_required
def manage_jobs_admin(request):
    profile = Profile.objects.get(user=request.user)

    # Only admin allowed here
    if profile.role.lower() != "admin":
        return redirect("manage_jobs_admin")

    if request.method == "POST":
        job = get_object_or_404(Job, id=request.POST["job_id"])
        action = request.POST["action"]

        if action == "approve":
            job.is_approved = True
        elif action == "reject":
            job.is_approved = False

        job.save()
        return redirect("manage_jobs_admin")

    jobs = Job.objects.all()

    return render(request, "manage_jobs_admin.html", {
        "jobs": jobs,
        "portal": "admin"
    })


@login_required
def add_job_alumni(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "alumni":
        return redirect("manage_jobs_admin")

    if request.method == "POST":
        Job.objects.create(
            title=request.POST.get("title"),
            company=request.POST.get("company"),
            description=request.POST.get("description"),
            posted_by=request.user
        )

    return redirect("manage_jobs_alumni")

@login_required
def add_job_admin(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "admin":
        return redirect("manage_jobs_alumni")

    if request.method == "POST":
        Job.objects.create(
            title=request.POST.get("title"),
            company=request.POST.get("company"),
            description=request.POST.get("description"),
            posted_by=request.user,
            # is_approved=True   # admin jobs auto-approved
        )

    return redirect("manage_jobs_admin")


@login_required
def edit_job_alumni(request, id):
    job = get_object_or_404(Job, id=id)
    profile = Profile.objects.get(user=request.user)

    # Alumni can edit ONLY their jobs
    if profile.role.lower() == "alumni" and job.posted_by != request.user:
        return redirect("manage_jobs_alumni")

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.company = request.POST.get("company")
        job.description = request.POST.get("description")
        job.save()

    return redirect("manage_jobs_alumni")

@login_required
def edit_job_admin(request, id):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "admin":
        return redirect("manage_jobs_alumni")

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.company = request.POST.get("company")
        job.description = request.POST.get("description")
        job.save()

    return redirect("manage_jobs_admin")


@login_required
def delete_job_alumni(request, id):
    job = get_object_or_404(Job, id=id)
    profile = Profile.objects.get(user=request.user)

    # Alumni can delete ONLY their jobs
    if profile.role.lower() == "alumni" and job.posted_by != request.user:
        return redirect("manage_jobs_alumni")

    if request.method == "POST":
        job.delete()

    if profile.role.lower() == "admin":
        return redirect("manage_jobs_admin")

    return redirect("manage_jobs_alumni")

@login_required
def delete_job_admin(request, id):
    profile = Profile.objects.get(user=request.user)

    if profile.role.lower() != "admin":
        return redirect("manage_jobs_alumni")

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":
        job.delete()

    return redirect("manage_jobs_admin")

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
    if request.user.profile.role.lower() != "admin":
        return redirect("login")

    events = Event.objects.all().order_by("-id")

    if request.method == "POST":
        event_id = request.POST.get("event_id")
        action = request.POST.get("action")

        event = get_object_or_404(Event, id=event_id)

        # ✏️ EDIT ONLY
        if action == "edit":
            event.title = request.POST.get("title")
            event.description = request.POST.get("description")
            event.date = request.POST.get("date")
            event.save()

        # ✅ APPROVE (NO TITLE CHANGE HERE)
        elif action == "approve":
            event.is_approved = True
            event.is_rejected = False
            event.save()

        # ❌ REJECT
        elif action == "reject":
            event.is_rejected = True
            event.is_approved = False
            event.save()

        return redirect("admin_events")

    return render(request, "admin_events.html", {"events": events})


