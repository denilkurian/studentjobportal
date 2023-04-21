from django.contrib.auth.models import User
from django.db import models


Qual = (
    ("Master", "Master"),
    ("Btech", "Btech"),
    ("Degree", "Degree"),
    ("Diploma", "Diploma"),
    ("Other", "Other"),
)

# Create your models here.
class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, choices=Qual, default='qualification')
    college = models.CharField(max_length=200)
    cgpa=models.IntegerField()
    experience=models.CharField(max_length=200)
    skills = models.TextField(max_length=200,default='Hard skills required.....Eg:Programming languages like Java,C++ etc')
    resume = models.FileField(upload_to='resume/',max_length=200,blank=True)
    profile = models.ImageField(upload_to='image/',max_length=100,blank=True)
    complete=models.BooleanField(default=False,blank=False)

    def __str__(self):
        return self.name



Type = (
    ("Information Technology", "Information Technology"),
    ("Business Management", "Business Management"),
    ("Sales Executive", "Sales Executive"),
    ("Accounting", "Accounting"),
    ("Health & Science", " Health & Science"),
    ("Architecture", "Architecture"),
    ("Education Careers", "Education Careers"),
)

Duration =(
    ("Full-time", "Full-time"),
    ("Half-time", "Half-time"),
)



class Jobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    job_type= models.CharField(max_length=200, choices=Type, default='IT field')
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    salary = models.CharField(max_length=150)
    duration = models.CharField(max_length=150,choices=Duration)
    job_description=models.TextField()
    complete=models.BooleanField(default=False)
    call=models.IntegerField()
    Hired=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.job_type

    class Meta:
        ordering = ["-created"]


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    header=models.CharField(max_length=50)
    about=models.TextField()
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.header




class Review(models.Model):
    product = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, choices=Qual, default='qualification')
    college = models.CharField(max_length=200)
    cgpa = models.IntegerField()
    experience = models.CharField(max_length=200)
    resume = models.FileField(upload_to='resume/')

    def __str__(self):
        return self.user



######## save options for job
class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



###################  companies

class Company(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    link = models.URLField()

