from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Student,Grade,Course,Teacher

import urllib
import datetime
import csv
import os
# Create your views here.


@csrf_protect
def login_view(request):
    nexturl=request.GET.get('next','')
    #return HttpResponse(nexturl)
    if request.method == 'POST':    
        username = request.POST.get('ID','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            if nexturl:
                return HttpResponseRedirect(nexturl)
            else:
                try:
                    teacher = request.user.teacher
                except:
                    return HttpResponseRedirect(reverse('selection.views.main'))
                else:
                    return HttpResponseRedirect(reverse('selection.views.teacher'))
        else:
              err="failed,id and password dont't match OR id isn't exist"
              return render_to_response('login.html',{'err':err},context_instance=RequestContext(request))
    else:
            return render_to_response('login.html',context_instance=RequestContext(request))


def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('selection.views.login_view'))


@login_required(login_url='/login/')
#@csrf_protect
def main(request):

    def deal_time():
        tmp = 0
        for course in selected_courses:
            if (1 << course.time) & tmp != 0:
                return "Time conflict!You can't have two courses at same time.Or this course \
                        you have alreay chose."
            tmp = tmp | (1 << course.time)
        if tmp & visitor.timetable != 0:
            return "Time conflict!You can't have two courses at same time.Or this course \
                        you have alreay chose."
        visitor.timetable = visitor.timetable | tmp
        #visitor.save()

    def get_timetable():
        table = [(['']*6) for i in range(5)]
        table[0][0] = '8:00-9:50'
        table[1][0] = '10:10-12:00'
        table[2][0] = '13:30-15:20'
        table[3][0] = '15:30-17:20'
        table[4][0] = '18:30-20:20'
        for c in cl:
            i = c.time % 5
            if i == 0: i = 5
            i -= 1
            j = c.time // 5 +1
            if j == 6: j=5
            table[i][j] = c.name+'#'+c.classroom
        return table

    def get_grade():
        '''
        目前没用
        '''
        return 1
        join_year = int(visitor.sid[:4])
        g = int(datetime.date.today[0:4])-join_year
        if int(datatime.date.today[5:7]) > 8 : g += 1
        return g
    try:
        visitor = request.user.student
    except:
        visitor =None
    is_delete = False

    
    if visitor:
        cl = visitor.courses.all()
        course1 = set(visitor.grade.course_set.all())
        course2 = set(visitor.major.course_set.all())
        course_list = course1 & course2
    else:
        course_list = []
        cl = []
    #course_list = Course.objects.all()
    err=[]

    if request.method == 'POST':
        is_delete = True#改动过student.courses的标志
        succ = []
        selected = []
        delete = []
        for key,value in request.POST.items() :
            if value == '1':
                selected.append(key)
            elif value == '2':
                delete.append(key)

        selected_courses = Course.objects.filter(id__in=selected)
        if selected_courses:
            d = deal_time()
            if d != None :
                if d not in err:
                    err.append(d)
            else:
                tmpl = list(selected_courses)
                tmpl.extend(list(visitor.courses.all() ))
                visitor.courses = tmpl 
                
                s = 'CHOOSE SUCEESS'
                if s not in succ:
                    succ.append(s)

        if delete:
            delete_courses = Course.objects.filter(id__in=delete)
            visitor.courses = list( set(visitor.courses.all()) -  set(delete_courses) )
            tmp = 0 
            for course in delete_courses:
                tmp = tmp | (1 << course.time )
            visitor.timetable = visitor.timetable & (~tmp)
           
            delete_message = 'DELETE SUCEESS'
            if delete_message not in succ:
                succ.append(delete_message)

        visitor.save()

        cl = visitor.courses.all()
        table = get_timetable()
        dic = {'course_list':course_list,
                'cl':cl,
                'err':err,
                'succ':succ,
                'table':table,
                'is_delete':is_delete,
                }

        return render_to_response('main.html',dic,
                                        context_instance=RequestContext(request))
    else:
        table =  get_timetable()
        dic = {'course_list':course_list,
                'cl':cl,
                'table':table,
                'is_delete':is_delete,
                }
        return render_to_response('main.html',dic,
                                        context_instance=RequestContext(request))

def teacher(request):
    err = []
    dic = {'err':err}
    if request.method == 'GET':
        try:
            teacher = request.user.teacher
        except :
            err.append('Sorry,You are not teacher')
        else:
            course_list = teacher.courses.all()
            dic[ 'course_list']=course_list
        return render_to_response('teacher.html',dic,
                                        context_instance=RequestContext(request))

def get_student_list(request):
    if request.method == 'POST':
        err = []
        course_sid = request.POST.get('course_sid','')
        if course_sid:
            try:
                course = Course.objects.get(sid=int(course_sid))
            except Exception as e:
                course = None
                print (e)
        else:
            course = None
        if course:
            students = course.student_set.all()
            print (len(students))
            filename = course_sid+'_'+'students.csv'
            filepath = '/tmp/'#临时存放生成的csv的路径
            with open(filepath+filename,'w') as f:
                writer = csv.writer(f)
                writer.writerow(('sid','name','class'))
                for student in students:
                    writer.writerow((student.sid, student.name, student.cla))

            with open(filepath+filename,'r') as f:
                content = f.read()
            encode_name = urllib.parse.quote(filename.encode('utf-8'))
            httpResponse = HttpResponse(content,content_type="application/octet-stream")
            #httpResponse["Content-Disposition"] = "attachment;filename=%s;filename*=%s" % (encode_name,encode_name)
            httpResponse["Content-Disposition"] = "attachment;filename=%s;" % (encode_name)
            httpResponse["Accept-Length"] = "%d" % (len(content))
            httpResponse["Accept-Ranges"] = "bytes"
            f = filepath+filename
            if os.path.exists(f):
                os.remove(f)
            else:
                print('f is not exist')
            return httpResponse
        else:
            err.append('Course is not exist.')
        dic={ 'err':err }
        return render_to_response('teacher.html', dic, context_instance=RequestContext(request) )
