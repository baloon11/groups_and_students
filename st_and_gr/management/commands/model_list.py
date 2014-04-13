from django.core.management.base import AppCommand
from st_and_gr.models import Groups,Students
from django.utils import translation
from django.conf import settings

# Usage   manage.py model_list st_and_gr ,where "st_and_gr" is app.name  
#The result of the work of the commands correctly displayed only in the windows-console (encoding 'Cp866')

class Command(AppCommand):

    requires_model_validation = True

    def handle_app(self, app, **options):
        translation.activate(settings.LANGUAGE_CODE)
        
        list_all=list()
        group_all=Groups.objects.all()
        group_list=[gr.id for gr in group_all] 
        for n in xrange(len(group_list)):              
            group=Groups.objects.get(pk=group_list[n])
            group_name_encode=(group.group_name).encode('Cp866') 
            list_all.append(group_name_encode+"\n")
            students_all=group.students_set.all() 
            students_list=[st.id for st in students_all] 
            for k in xrange(len(students_list)):                 
                student_for_write=Students.objects.get(pk=students_list[k])
                full_name_encode=(student_for_write.full_name).encode('Cp866')                   
                list_all.append(full_name_encode+"\n")         
        list_all[0]="-------------------------"+"\n"+list_all[0]  
        list_all[-1]=list_all[-1]+"\n"+"-------------------------"         
        translation.deactivate() 
        return "".join(list_all)        
           
             
            
            
                           

        
        
        
        

            

