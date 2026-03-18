import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Profile,Event,Job,Announcement
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Profile
from .filters import AlumniFilter


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

        username = request.POST.get("username") 

        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("alumni_dashboard")

        else:
            return render(request, "alumni_login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "alumni_login.html")


def logout_view(request):
    logout(request)
    return redirect("login_portal")


def alumni_register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user = user,
            role = "alumni"
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

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        form = EditProfile(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("alumni_dashboard")

        else:
            print(form.errors)

    else:
        form = EditProfile(instance=profile)

    return render(request, "edit_profile.html", {"form": form})


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

        # user already exist check
        if User.objects.filter(username=username).exists():
            return render(request, "alumni_register.html", {
                "error": "User already exists. Please login."
            })

        # create new user
        User.objects.create_user(
            username=username,
            password=password
        )

        # after register go to login page
        return redirect("alumni_login")

    return render(request, "alumni_register.html")

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
    profile = request.user.profile

    if request.method == "POST":
        profile.roll_no = request.POST.get("roll_no")
        profile.email = request.POST.get("email")
        profile.designation = request.POST.get("designation")
        profile.remarks = request.POST.get("remarks")
        profile.department = request.POST.get("department")
        profile.address = request.POST.get("address")
        profile.current_job = request.POST.get("current_job")
        profile.company = request.POST.get("company")
        profile.location = request.POST.get("location")
        profile.phone = request.POST.get("phone")
        profile.alternate_phone = request.POST.get("alternate_phone")

        profile.role = request.POST.get("role")
        profile.linkedin_profile = request.POST.get("linkedin_profile")
        profile.google_scholar = request.POST.get("google_scholar")

        full_name = request.POST.get("full_name")
        if full_name:
            request.user.username = full_name
            request.user.save()

        join_year = request.POST.get("join_year")
        if join_year and join_year != "None":
            profile.join_year = int(join_year)
        # else:
        #     profile.join_year = None

        passout_year = request.POST.get("passout_year")
        if passout_year and passout_year != "None":
            profile.passout_year = int(passout_year)
        # else:
        #     profile.passout_year = None

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get("profile_image")

        if request.FILES.get("proof_id"):
            profile.proof_id = request.FILES.get("proof_id")

        if request.FILES.get("company_id_image"):
            profile.company_id_image = request.FILES.get("company_id_image")

        if request.FILES.get("appointment_order"):
            profile.appointment_order = request.FILES.get("appointment_order")

        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("alumni_dashboard")

    return redirect("alumni_dashboard")

def superuser_required(user):
    return user.is_superuser


@login_required

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


def admin_view_alumni(request):
    q = request.GET.get('q', '').strip()
    
    # Start with all profiles and optimize with select_related
    profiles = Profile.objects.select_related('user').all()

    if q:
        # 1. Handle Year Filters (Try to convert query to int for exact year matches)
        year_q = None
        try:
            year_q = int(q)
        except ValueError:
            pass

        # 2. Build the Filter Query
        # This covers every visible field in your HTML table
        query_filter = (
            Q(user__username__icontains=q) |
            Q(role__icontains=q) |
            Q(roll_no__icontains=q) |
            Q(email__icontains=q) |
            Q(department__icontains=q) |
            Q(designation__icontains=q) |
            Q(current_job__icontains=q) |
            Q(company__icontains=q) |
            Q(location__icontains=q) |
            Q(phone__icontains=q) |
            Q(alternate_phone__icontains=q) |
            Q(linkedin_profile__icontains=q) |
            Q(google_scholar__icontains=q)
        )

        # 3. Add Year filters if the query is numeric
        if year_q:
            query_filter |= Q(join_year=year_q) | Q(passout_year=year_q)
        else:
            # Also check icontains for years if they are stored as strings/charfields
            query_filter |= Q(join_year__icontains=q) | Q(passout_year__icontains=q)

        profiles = profiles.filter(query_filter).distinct()

    # AJAX Response Logic
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for p in profiles:
            data.append({
                "username": p.user.username if p.user else "",
                "role": p.role or "",
                "roll_no": p.roll_no or "",
                "email": p.email or "",
                "department": p.department or "",
                "join_year": p.join_year or "",
                "passout_year": p.passout_year or "",
                "designation": p.designation or "",
                "current_job": p.current_job or "",
                "company": p.company or "",
                "location": p.location or "",
                "phone": p.phone or "",
                "alternate_phone": p.alternate_phone or "",
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

    alumni_queryset = Profile.objects.filter(role__iexact="alumni").select_related("user")
    print("All Alumni:", alumni_queryset.count())

    alumni_filter = AlumniFilter(request.GET, queryset=alumni_queryset)

    # filtered_qs = alumni_filter.qs.order_by("-created_at", "-passout_year")
    filtered_qs = alumni_filter.qs.order_by("-created_at")
    print("Filtered Alumni:", filtered_qs.count())

    paginator = Paginator(filtered_qs, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    print("Page Objects:", page_obj)

    return render(
        request,
        "admin_view_alumni.html",
        {
            "filter": alumni_filter,
            "page_obj": page_obj,
        },
    )

    
    

@login_required
def admin_edit_alumni(request, pk):

    alumni = get_object_or_404(Profile, pk=pk)

    if request.method == "POST":

        form = AlumniEditForm(request.POST, request.FILES, instance=alumni)

        if form.is_valid():
            form.save()
            return redirect("admin_view_alumni")

    else:

        form = AlumniEditForm(instance=alumni)

    return render(
        request,
        "admin_edit_alumni.html",
        {
            "form": form,
            "alumni": alumni,
        },
    )    



    
@login_required
def admin_add_alumni(request):

    if request.method == "POST":

        form = AlumniCreateForm(request.POST, request.FILES)

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=username,
                password=password
            )

            profile = form.save(commit=False)
            profile.user = user
            profile.role = "alumni"
            profile.save()

            return redirect("admin_view_alumni")

    else:

        form = AlumniCreateForm()

    return render(
        request,
        "admin_add_alumni.html",
        {
            "form": form
        },
    )
    



@login_required
def admin_view_user(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":

        new_password = request.POST.get("password")

        if new_password:
            user.set_password(new_password)
            user.save()

            return redirect("admin_view_user", pk=user.id)

    return render(
        request,
        "admin_view_user.html",
        {
            "user": user,
            "profile": user.profile
        }
    )
    
    
    
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


@login_required
def edit_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.date = request.POST.get("date")
        event.save()

    return redirect("create_event")


@login_required
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

@login_required

def edit_announcement(request, id):

    announcement = get_object_or_404(Announcement, id=id)

    if request.method == "POST":

        announcement.title = request.POST.get('title')
        announcement.message = request.POST.get('message')

        announcement.save()

    return redirect('announcements_page')




# DELETE ANNOUNCEMENT

@login_required

def delete_announcement(request, id):

    announcement = get_object_or_404(Announcement, id=id)

    announcement.delete()

    return redirect('announcements_page')


@login_required
def jobs_alumni(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if (profile.role or "").lower() != "alumni":
        return redirect("index")

    if request.method == "POST":
        Job.objects.create(
            title=request.POST["title"],
            company=request.POST["company"],
            description=request.POST["description"],
            posted_by=request.user
        )
        return redirect("jobs_alumni")

    jobs = Job.objects.all().order_by("-posted_on")

    return render(request, "jobs_alumni.html", {"jobs": jobs})


@login_required
def jobs_admin(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Only admin allowed here
    if (profile.role or "").lower() != "admin":
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
    profile, created = Profile.objects.get_or_create(user=request.user)

    if (profile.role or "").lower() != "alumni":
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
def edit_job_alumni(request, id):
    job = get_object_or_404(Job, id=id)
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Alumni can edit ONLY their jobs
    if (profile.role or "").lower() == "alumni" and job.posted_by != request.user:
        return redirect("jobs_alumni")

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.company = request.POST.get("company")
        job.description = request.POST.get("description")
        # job.location = request.POST.get("location")
        job.save()

    return redirect("jobs_alumni")


@login_required
def delete_job_alumni(request, id):
    job = get_object_or_404(Job, id=id)

    if job.posted_by != request.user:
        return redirect("jobs_alumni")

    job.delete()
    return redirect("jobs_alumni")


@login_required
def admin_announcements(request):
    announcements = Announcement.objects.all()
    return render(request, "admin_announcements.html", {"announcements": announcements})


def alumni_announcements(request):
    announcements = Announcement.objects.all().order_by('-posted_on')
    return render(request, 'alumni_announcements.html', {
        'announcements': announcements
    })


@login_required
def manage_admin_events(request):

    profile, created = Profile.objects.get_or_create(user=request.user)

    if not request.user.is_superuser:
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

