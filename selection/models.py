from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Grade(models.Model):
    '''
    年级
    name为大一、大二或者1、2这样的名称
    '''
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Major(models.Model):
    '''
    专业
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    '''
    课程
    compulsory:是否是选修课，True/False
    name:名称
    sid:课程id
    power:学分
    time:在课程表上的位置，合法值为1-25
    classrrom：上课教室
    content：课程描述
    '''
    
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
    '''
    教师
    sid:教师编号
    name:教师姓名
    '''
    
    sid = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    user = models.OneToOneField(User)
    courses = models.ManyToManyField(Course,blank=True)
    def __str__(self):
        return self.name


class Student(models.Model):
    '''
    学生
    name:学生姓名
    sid:学号
    cla:班级
    timetable:时间表，采用位运算。转化成二进制从低到高第i位上数字为1
    说明此时间段已经有课
    
    '''
    
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


