from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now



class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, default=1)
    status = models.IntegerField(default=0)          # Approval
    is_verified = models.BooleanField(default=False) # Verification



class Seeker(models.Model):
    EDUCATION_CHOICES = (
        ('SSLC', 'SSLC'),
        ('PLUS_TWO', 'Plus Two'),
        ('DIPLOMA', 'Diploma'),
        ('UG', 'Under Graduate'),
        ('PG', 'Post Graduate'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=15)
    dob = models.DateField()

    education = models.CharField(
        max_length=50,
        choices=EDUCATION_CHOICES,
        null=True,
        blank=True
    )
    certifications = models.TextField(blank=True)

    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True
    )

    # ✅ NEW FIELDS
    profile_picture = models.ImageField(
        upload_to='seeker_profiles/',
        null=True,
        blank=True
    )

    address = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username



class Employer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    company_name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=15)

    logo = models.ImageField(
        upload_to='company_logos/',
        null=True,
        blank=True
    )
    website = models.URLField(null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return self.company_name




class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    )

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    designation = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    last_date = models.DateField()
    posted_date = models.DateField(auto_now_add=True)

    status = models.IntegerField(default=0)
    admin_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.designation




class Application(models.Model):
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Viewed', 'Viewed'),
         ('Profile Visited', 'Profile Visited'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    admin_seen = models.BooleanField(default=False)


    class Meta:
        unique_together = ('seeker', 'job')  # prevent duplicate apply

    def __str__(self):
        return f"{self.seeker.user.username} → {self.job.designation}"


class SeekerNotification(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



class SeekerNotificationPreference(models.Model):
    seeker = models.OneToOneField(Seeker, on_delete=models.CASCADE)
    preferred_company = models.CharField(max_length=100, blank=True)
    preferred_title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.seeker.user.username
