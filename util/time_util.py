import time


#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
class Time:
    def __init__(self):
        self.time_obj = time.localtime()

    @property
    def date_str(self):
        return time.strftime('%Y%m%d', self.time_obj)

    @property
    def time_str(self):
        return time.strftime('%H%M%S', self.time_obj)


#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def now():
    return time.localtime()

#def getDateStr(time_obj):
#    date_str = time.strftime('%Y%m%d', time_obj)
#    time_str = time.strftime('%H%M%S', time_obj)
#
#    return (date_str, time_str)
#
#def getNowDateTimeStr():
#    now = time.localtime()
#    date_str = time.strftime('%Y%m%d', now)
#    time_str = time.strftime('%H%M%S', now)
#
#    return (date_str, time_str)

#-------------------------------------------------------------------------------
def timestamp():
    result = time.strftime("%Y/%m/%d (%a) %H:%M:%S", now())
    return result
