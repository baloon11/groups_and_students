# coding: utf-8
from django.contrib import admin
from st_and_gr.models import Groups,Students,Info_About_Models
from django.contrib.auth.models import User

class Students_Admin(admin.ModelAdmin):
    list_display=('id','full_name','student_id_number','group') 

class StudentsInline(admin.TabularInline):
    model = Students                  

class Groups_Admin(admin.ModelAdmin):
    inlines = [StudentsInline,]
    list_display=('id','group_name',)


admin.site.register(Students, Students_Admin)
admin.site.register(Groups,Groups_Admin)
admin.site.register(Info_About_Models)
   