from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()

    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    posted_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    def get_image_url(self):
        title = self.title.lower()

        if "developer" in title or "software" in title or "programmer" in title:
            return "https://cdn-icons-png.flaticon.com/512/2721/2721296.png"

        elif "designer" in title or "ui" in title or "ux" in title:
            return "https://cdn-icons-png.flaticon.com/512/2920/2920277.png"

        elif "manager" in title or "lead" in title:
            return "https://cdn-icons-png.flaticon.com/512/1995/1995574.png"

        elif "tester" in title or "qa" in title:
            return "https://cdn-icons-png.flaticon.com/512/1055/1055687.png"

        elif "intern" in title or "trainee" in title:
            return "https://cdn-icons-png.flaticon.com/512/201/201818.png"

    # 🔹 NEW JOB TYPES 🔹
        elif "data" in title or "analyst" in title:
            return "https://cdn-icons-png.flaticon.com/512/2782/2782058.png"

        elif "marketing" in title or "seo" in title or "digital" in title:
            return "https://cdn-icons-png.flaticon.com/512/1998/1998610.png"

        elif "hr" in title or "recruiter" in title:
            return "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

        elif "network" in title or "system" in title or "admin" in title:
            return "https://cdn-icons-png.flaticon.com/512/4248/4248443.png"

        elif "security" in title or "cyber" in title:
            return "https://cdn-icons-png.flaticon.com/512/3064/3064197.png"

        else:
            return "https://cdn-icons-png.flaticon.com/512/847/847969.png"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10,
        default='alumni',
        blank=True, null=True
    )
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    roll_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    appointment_order = models.CharField(max_length=150, blank=True, null=True)

    proof_id = models.FileField(upload_to="id", max_length=100, blank=True, null=True)
    
    remarks = models.TextField(blank=True, null=True)
    
    department = models.CharField(max_length=100, blank=True, null=True)
    
    join_year = models.IntegerField(blank=True, null=True)
    passout_year = models.IntegerField(blank=True, null=True)
    
    address = models.TextField(blank=True, null=True)
    
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    
    current_job = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.passout_year}"
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    image_url = models.URLField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.title:   # ✅ SAFE CHECK
            title_lower = self.title.lower()

            # 🔴 OLD RULES (UNCHANGED)
            if "job" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4"

            elif "tech" in title_lower or "ai" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1519389950473-47ba0277781c"

            elif "alumni" in title_lower or "meet" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1523580494863-6f3031224c94"

            elif "sports" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1508609349937-5ec4ae374ebf"

            elif "startup" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1559136555-9303baea8ebd"

        # 🆕 NEW EVENTS (ADDED — NOT REMOVING OLD)

        # 🎭 Cultural Fest / Celebration
            elif "cultural" in title_lower or "fest" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"

        # 🎓 Higher Studies / Abroad / Seminar
            elif "higher studies" in title_lower or "abroad" in title_lower or "seminar" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f"

        # 🏫 Workshop / Training
            elif "workshop" in title_lower or "training" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1522202176988-66273c2fd55f"

        # 🧠 Webinar / Guest Lecture
            elif "webinar" in title_lower or "guest lecture" in title_lower or "talk" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3"

        # 🌍 Social / Community Event
            elif "social" in title_lower or "community" in title_lower or "volunteer" in title_lower:
                self.image_url = "https://images.unsplash.com/photo-1509099836639-18ba1795216d"

        # 🔁 FINAL FALLBACK (IF NOTHING MATCHES)
            else:
                self.image_url = "https://images.unsplash.com/photo-1506784983877-45594efa4cbe"

        super().save(*args, **kwargs)




# 🔹 ANNOUNCEMENT
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    image_url = models.URLField(blank=True)
    posted_on = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.image_url or self.image_url.strip() == "":
            self.image_url = "https://img.freepik.com/premium-vector/megaphone-with-announcement-speech-bubble-banner-loudspeaker_1027249-725.jpg"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
