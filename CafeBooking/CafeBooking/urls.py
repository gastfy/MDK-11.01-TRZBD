"""
URL configuration for CafeBooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import include, path
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from .views import delete_rs_archived, book_qr_code, admin_page, __download_qrcodes, head_panel, settings, user_reservations, success, book, set_archive_time, reservations, menu, reg_page, login_page, add_entity, edit_entity, delete_entity, ban_user, cancel_reservation, unban_user, homepage, download_report, create_dump, upload, profile, logout, delete_account, update_user
from django.http import HttpResponse, HttpResponseRedirect
from .tasks import Status, Time
from .views import log, cancel, continue_reservation

def init():
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
        
    if Status.objects.filter(status = "Отменено").exists() is False:
        status = Status()
        status.status = "Отменено"
        status.save()
        log(f"Статус '{status.status}' создан!")
        
    if Time.objects.filter(time = "Утреннее").exists() is False:
            time__ = Time()
            time__.time = "Утреннее"
            time__.save()
    
    if Time.objects.filter(time = "Вечернее").exists() is False:
            time__ = Time()
            time__.time = "Вечернее"
            time__.save()
        
    if Time.objects.filter(time = "Весь день").exists() is False:
            time__ = Time()
            time__.time = "Весь день"
            time__.save()

def metrics_view(request):
    metrics = generate_latest()
    return HttpResponse(metrics, content_type=CONTENT_TYPE_LATEST)

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', admin_page),
    path('login/', login_page),
    path('reg/', reg_page),
    path('admin/add/', add_entity),
    path('admin/edit/', edit_entity),
    path('admin/delete/', delete_entity),
    path('admin/ban/', ban_user),
    path('admin/unban/', unban_user),
    path('admin/cancel/', cancel_reservation),
    path('download-report/', download_report),
    path('admin/create-dump/', create_dump),
    path('admin/upload/', upload),
    path('admin/set-archive-time/', set_archive_time),
    path('profile/', profile),
    path('logout/', logout),
    path('delete/', delete_account),
    path('edit/', update_user),
    path('menu/', menu),
    path('reservations/', reservations),
    path('book/<int:id>/', book),
    path('success/', success),
    path('user-reservations/', user_reservations),
    path('cancel/<int:id>/', cancel),
    path('continue/<int:id>/', continue_reservation),
    path('settings/', settings),
    path("head-panel/", head_panel),
    path("download-qrcodes/", __download_qrcodes),
    path('qr_book/<int:id>/', book_qr_code),
    path('delete-archivated/', delete_rs_archived),
    path('', include('django_prometheus.urls')),
    path('', homepage),
]

