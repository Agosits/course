from django import template
register = template.Library()
@register.filter
def  time_trans(t):
    if t == 0 :
        return 'time is not set'
    count = t
    weekday = count // 5
    r = count%5
    if r == 0:
        weekday -= 1
    tup = ('Mon','Tues','Wed','Thur','Fri')
    s = tup[weekday]
    timelist = ('18:00-20:20','8:00-9:50','10:10-12:00','13:30-15:20',
                    '15:30-17:20')
    s = s + ',' +timelist[r]
    return s