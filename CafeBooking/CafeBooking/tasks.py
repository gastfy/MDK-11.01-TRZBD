from huey.contrib.djhuey import db_periodic_task
from huey.contrib.djhuey import periodic_task
from huey import crontab, RedisHuey
from .models import Reservation, User, Status, Time
from .views import log
import datetime
import pytz
from django.utils import timezone

def calculate_utc_time(local_time):
    return local_time.astimezone(datetime.UTC)

local_time_morning = timezone.datetime(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day, hour=14, minute=0)
utc_time_morning = calculate_utc_time(local_time_morning)

local_time_evening = timezone.datetime(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day, hour=19, minute=0)
utc_time_evening = calculate_utc_time(local_time_evening)

local_time_end = timezone.datetime(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day, hour=23, minute=0)
utc_time_end = calculate_utc_time(local_time_end)


@db_periodic_task(crontab(hour=f"{utc_time_morning.hour}", minute=f"{utc_time_morning.minute}"), retries=2, retry_delay=240)
def morning_check():
    
    print("MORNING task start at: ", datetime.datetime.now())
    
    today = datetime.date.today()
    time = datetime.datetime.now().time()
    
    if time < datetime.time(14, 0):
        print("MORNING -- preexuceted at: ", datetime.datetime.now())
        return
    
    if Status.objects.filter(status = "Забронировано").exists() is False:
            status = Status()
            status.status = "Забронировано"
            status.save()
            log(f"Статус '{status.status}' создан!")
            
    if Status.objects.filter(status = "Завершено").exists() is False:
            status = Status()
            status.status = "Завершено"
            status.save()
            log(f"Статус '{status.status}' создан!")
        
    if Time.objects.filter(time = "Утреннее").exists() is False:
        time__ = Time()
        time__.time = "Утреннее"
        time__.save()
        
    reserved_status = Status.objects.filter(status = "Забронировано").first()
    finished_status = Status.objects.filter(status = "Завершено").first()
    time = Time.objects.filter(time = "Утреннее").first()
        
    reservations = Reservation.objects.filter(status=reserved_status, date=today, time=time)
    for rs in reservations:
        rs.status = finished_status
        rs.save()
    
    print("MORNING task successfully end!")



@db_periodic_task(crontab(hour=f"{utc_time_evening.hour}", minute=f"{utc_time_evening.minute}"), retries=2, retry_delay=240)
def evening_check():
    today = datetime.date.today()
    
    time = datetime.datetime.now().time()
    
    print("EVENING task start at: ", datetime.datetime.now())
    
    if time < datetime.time(19, 0):
        print("EVENING -- preexecuted at: ", datetime.datetime.now())
        return
    
    
    if Status.objects.filter(status = "Забронировано").exists() is False:
            status = Status()
            status.status = "Забронировано"
            status.save()
            log(f"Статус '{status.status}' создан!")
            
    if Status.objects.filter(status = "Завершено").exists() is False:
            status = Status()
            status.status = "Завершено"
            status.save()
            log(f"Статус '{status.status}' создан!")
        
    if Time.objects.filter(time = "Вечернее").exists() is False:
        time__ = Time()
        time__.time = "Вечернее"
        time__.save()
        
    reserved_status = Status.objects.filter(status = "Забронировано").first()
    finished_status = Status.objects.filter(status = "Завершено").first()
    time = Time.objects.filter(time = "Вечернее").first()
    
    reservations = Reservation.objects.filter(status=reserved_status, date=today, time=time)
    for rs in reservations:
        rs.status = finished_status
        rs.save()
    
    print("EVENING task successfully end!")
        
        
@db_periodic_task(crontab(hour=f"{utc_time_end.hour}", minute=f"{utc_time_end.minute}"), retries=2, retry_delay=240)
def not_handled_finish():
    
    today = datetime.date.today()
    
    time = datetime.datetime.now().time()
    
    print("NOT_HANDLED task start at: ", datetime.datetime.now())
    
    if time < datetime.time(23):
        print("NOT_HANDLED -- preexecuted at: ", datetime.datetime.now())
        return
    
    if Status.objects.filter(status = "Забронировано").exists() is False:
            status = Status()
            status.status = "Забронировано"
            status.save()
            log(f"Статус '{status.status}' создан!")
            
    if Status.objects.filter(status = "Завершено").exists() is False:
            status = Status()
            status.status = "Завершено"
            status.save()
            log(f"Статус '{status.status}' создан!")
        
    reserved_status = Status.objects.filter(status = "Забронировано").first()
    finished_status = Status.objects.filter(status = "Завершено").first()    
    
    reservations = Reservation.objects.filter(status=reserved_status, date__lte=today)
    for rs in reservations:
        rs.status = finished_status
        rs.save()
    
    print("NOT HANDLED task successfully executed!")
        

@periodic_task(crontab(minute='*/5'))
def ping():
    print("ping at: ", datetime.datetime.now())