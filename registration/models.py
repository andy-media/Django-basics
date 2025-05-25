from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    is_school_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class School(models.Model):
    REGION_CHOICES = (
        ('Accra', 'Greater Accra'),
        ('Central', 'Central'),
        ('Western', 'Western'),
        ('Northern', 'Northern'),
        ('Ashanti', 'Ashanti'),
        ('Eastern', 'Eastern'),
        ('Volta', 'Volta'),
        ('Ahafo', 'Ahafo'),
        ('Bono', 'Bono'),
        ('Bono East', 'Bono East'),
        ('Upper East', 'Upper East'),
        ('Upper West', 'Upper West'),
        ('Savannah', 'Savannah'),
        ('North East', 'North East'),
        ('Oti', 'Oti'),
        ('Western North', 'Western North'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='school')
    name_of_school = models.CharField(max_length=200)
    region = models.CharField(max_length=20, choices=REGION_CHOICES, default="Not Selected")
    location = models.CharField(max_length=200)
    school_head_name = models.CharField(max_length=100)
    school_contact = models.CharField(max_length=20, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    
    registration_complete = models.BooleanField(default=False)
    payment_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name_of_school

class Contestant(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='contestants')
    name = models.CharField(max_length=100, null=True, blank=True)
    year_form = models.CharField(max_length=50, null=True, blank=True)
   

    
    def __str__(self):
        return f"{self.name} ({self.year_form})"

class Coach(models.Model):
    COACH_TYPES = (
        ('science', 'Science Coach'),
        ('maths', 'Maths Coach'),
        ('computing', 'Computing Coach'),
    )
    
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='coaches')
    coach_type = models.CharField(max_length=20, choices=COACH_TYPES)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=20, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])

    class Meta:
        unique_together = ('school', 'coach_type')
    
    def __str__(self):
        return f"{self.get_coach_type_display()}: {self.name}"

class Payment(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paystack_ref = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment #{self.id} - {self.school.name_of_school}"
    


# models.py
class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
