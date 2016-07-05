from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Grade(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Major(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    compulsory = models.BooleanField(default='False')
    name = models.CharField(max_length=100)
    sid = models.CharField(max_length=20)
    power = models.IntegerField(null=True)
    time = models.IntegerField(default=0)
    classroom = models.CharField(max_length=10,default='0-000')
    content = models.CharField(max_length=100,blank=True)

    grades = models.ManyToManyField(Grade)
    majors = models.ManyToManyField(Major)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('sid',)


class Teacher(models.Model):
    sid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    user = models.OneToOneField(User)
    courses = models.ManyToManyField(Course,blank=True)
    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    sid = models.CharField(max_length=12)
    cla = models.CharField(max_length=10)
    timetable = models.IntegerField(default=0)
    
    courses = models.ManyToManyField(Course,blank=True)
    user = models.OneToOneField(User)
    grade = models.ForeignKey(Grade,blank=True,null=True)
    major = models.ForeignKey(Major,blank=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ('sid',)


