from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Profile
from .filters import AlumniFilter


def index(request):

    alumni_count = Profile.objects.filter(role="alumni").count()
    event_count = Event.objects.count()
    # job_count = Job.objects.count()
    announcement_count = Announcement.objects.count()

    context = {
        "alumni_count": alumni_count,
        "event_count": event_count,
        # "job_count": job_count,
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


@login_required
def admin_view_alumni(request):

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

    if (profile.role or "").lower() != "admin":
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
