from django.contrib import admin
from . models import Doctor,Department,Slots,Appointment,Booking_Notification,Services
# Register your models here.
class SlotsAdmin(admin.ModelAdmin):
    list_display = ('id','doctor', 'date', 'start_time', 'end_time', 'status', 'slot_duration', 'is_booked')
    

class AppointmentAdmin(admin.ModelAdmin):
    list_display=('patient','doctor','status','slot')
    



admin.site.register(Doctor)
admin.site.register(Services)
admin.site.register(Booking_Notification)

admin.site.register(Department)
admin.site.register(Slots, SlotsAdmin)
admin.site.register(Appointment,AppointmentAdmin)
