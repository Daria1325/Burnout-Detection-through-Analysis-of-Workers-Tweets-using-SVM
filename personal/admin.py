from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from personal.models import State, Employee, Result, Username

admin.site.register(Username)


class StateAdmin(admin.ModelAdmin):
    list_display = ('status','progress','note')
    search_fields = ('status','progress')
    readonly_fields = ()
    ordering = ('status',)

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()
    # username = None
    # USERNAME_FIELD = 'status'
    # REQUIRED_FIELDS = []
admin.site.register(State, StateAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name','sex','birth_date','join_date','position','avatar','state_id', 'email')
    search_fields = ('name','position')
    readonly_fields = ()
    ordering = ('name',)

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()
admin.site.register(Employee, EmployeeAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('employee_id','scan_date','percent_N','percent_S','percent_L','count_N','count_S','count_L', 'status')
    search_fields = ('employee_id','scan_date', 'status')
    readonly_fields = ()
    ordering = ('employee_id','scan_date')

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()
admin.site.register(Result, ResultAdmin)
