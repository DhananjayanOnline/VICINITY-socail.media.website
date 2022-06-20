from datetime import timedelta, datetime

from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

# utype = (
#     ("New Department", "New Department"),
#     ("user","user"),
# )

class UserReg(models.Model):
    uid = models.IntegerField(primary_key=True)
    username = models.CharField("Username : ", max_length=30, unique=True)
    password = models.CharField("Password : ", max_length=15)
    email = models.EmailField("Email :")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$',
                                 message="phone number must be entered in the format: '+91'. Up to 12 digital allowed.")
    phone_number = models.CharField("Phone number :", validators=[phone_regex], max_length=17, blank=False)
    panchayath = models.CharField("Enter your panchayath : ", max_length=30)
    district = models.CharField("Enter your district : ", max_length=30)
    state = models.CharField("Enter your state : ", max_length=30)
    country = models.CharField("Enter your country " , max_length=30)
    fname = models.CharField("First Name : ", max_length=30)
    lname = models.CharField("Last Name : ", max_length=30)
    house_name = models.CharField("House Name : ", max_length=50)
    house_number = models.IntegerField("House Number : ")
    gender = models.CharField("Gender : ", max_length=20)
    dob = models.DateField("Date of Birth : yyyy-mm-dd")
    photo = models.ImageField(upload_to='images/')

class DeptReg(models.Model):
    did = models.IntegerField(primary_key=True)
    username = models.CharField("Username : ", max_length=30, unique=True)
    password = models.CharField("Password : ", max_length=15)
    email = models.EmailField("Email :")
    department = models.CharField("Department : ", max_length=30)
    panchayath = models.CharField("Enter your panchayath : ", max_length=30)
    district = models.CharField("Enter your district : ", max_length=30)
    state = models.CharField("Enter your state : ", max_length=30)
    country = models.CharField("Enter your country ", max_length=30)
    photo = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=20, default='new department')

class Post(models.Model):
    postid = models.AutoField(primary_key=True)
    creatorid = models.IntegerField(null=True, blank=True)
    creator = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    panchayath = models.CharField(max_length=40)
    # photo = models.ImageField(upload_to='images/', default='x', null=True, blank=True)
    pimage = models.ImageField(upload_to='images/')
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    commentcount = models.IntegerField(default=0)

    class Meta:
        ordering = ['-postid']

class Comments(models.Model):
    commentid = models.IntegerField(primary_key=True)
    postid = models.IntegerField()
    commentatorid = models.IntegerField()
    commentator = models.CharField(max_length=30)
    comment = models.CharField(max_length=500)



class Vote(models.Model):
    postid = models.IntegerField()
    userid = models.IntegerField(null=True)
    username = models.CharField(max_length=30)
    upvotestatus = models.IntegerField(default=0)
    downvotestatus = models.IntegerField(default=0)

class Message(models.Model):
    mid = models.IntegerField(primary_key=True)
    senderid = models.IntegerField()
    receiverid = models.IntegerField()
    sendername = models.CharField(max_length=30)
    receivername = models.CharField(max_length=30)
    panchayath = models.CharField(max_length=100)
    message = models.CharField(max_length=300, null=True, blank=True)
    class Meta:
        ordering = ['-mid']


class Complaints(models.Model):
    cid = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    uname = models.CharField(max_length=30)
    panchayath = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    complaint = models.TextField(max_length=300)

    class Meta:
        ordering = ['-cid']

class Announcement(models.Model):
    aid = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    uname = models.CharField(max_length=30)
    panchayath = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    announcement = models.TextField(max_length=300, default='x')
    created = models.DateField(default=datetime.now())
    expiry = models.DateField(default=datetime.now()+timedelta(days=2))

    class Meta:
        ordering = ['-aid']