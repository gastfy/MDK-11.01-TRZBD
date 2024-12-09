from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Time)
admin.site.register(Status)
admin.site.register(Office)
admin.site.register(Place)
admin.site.register(Type)
admin.site.register(Reservation)
