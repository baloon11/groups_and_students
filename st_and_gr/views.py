# coding: utf-8
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

from st_and_gr.models import Groups,Students,Info_About_Models
from st_and_gr.forms import Start_Form,Reg_Form,Create_Group_Form,Edit_Group_Form,Student_Form,Edit_Student_Form
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView 
from django.views.generic.base import TemplateView
from django.contrib import auth

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random

class Start(FormView):
    form_class = Start_Form   
    template_name = 'start.html'    
   
    def form_valid(self, form):
        c_d_f = form.cleaned_data
        if '@' in c_d_f['username']:
            if User.objects.filter(email=c_d_f['username']).exists(): 
                us_name=User.objects.get(email=c_d_f['username'])
                user=auth.authenticate(username=us_name.username, password=c_d_f['password'])
            else:  
                return render_to_response("start.html",{'error_start':'Очевидно, вы неверно ввели логин/email или пароль. Повторите попытку'},
                                           context_instance=RequestContext(self.request))       
        else:
            user = auth.authenticate(username=c_d_f['username'], password=c_d_f['password'])          
       
        if user is not None:
            auth.login(self.request, user)        
            return HttpResponseRedirect('groups_list/')
        else:
            return render_to_response("start.html",{'error_start':'Очевидно, вы неверно ввели логин/email или пароль. Повторите попытку'},
                                       context_instance=RequestContext(self.request))


class Registration(FormView):
    form_class = Reg_Form     
    template_name = 'registration.html'

    def form_valid(self, form):
        c_d_f = form.cleaned_data
        user = User.objects.create_user(username=c_d_f['username'],email=c_d_f['email'], password=c_d_f['password'])
        user.is_staff = False
        user.save()
        user = auth.authenticate(username= c_d_f['username'], password= c_d_f['password'] )
        if user is not None:                                
            auth.login(self.request, user)             
        return HttpResponseRedirect('/')
         
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')     
      
class Groups_List(ListView): 
    model=Groups                    
    template_name='groups_list.html'
    context_object_name = 'groups_list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Groups_List, self).dispatch(*args, **kwargs)
  
class Create_Group(CreateView):
    form_class =Create_Group_Form  
    template_name = 'create_group.html'

    def form_valid(self, form):    
        c_d_f = form.cleaned_data                                           
        st_list=Students.objects.all() #находим всех студентов 
        rand=random.randint(0,st_list.count()-1 ) # выводим случайное число из диапазона от 0 до последнего индекса
                                                   # в списке(охвытываем весь список)
        st_list=st_list[rand] # находим число с таким индексом в списке (таким образом исключаем появления 0 в результате)
        st_rand=Students.objects.get( id=st_list.id) #находим случайного студента 
        Groups.objects.create( group_name=c_d_f['group_name'], headman_id=st_rand.id )
        # создаем новую группу (староста -случайный студент ) 
        #   первый студент  записанный в эту группу станет старостой -- реализовано в Add_Student                                              
        return HttpResponseRedirect (reverse('groups_list'))             

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Create_Group, self).dispatch(*args, **kwargs)              
      
def now_used_group(requst,pk):  
#представление-прослойка; записывает инф.в поле now_used (модель Group)
#и перенаправляет работу на Edit_Group
#Эта записанная инф. используется для правильного формирования выпадающего списка в форме Edit_Group_Form
    for gr in Groups.objects.all():
        gr.now_used=False   
        gr.save()
    group_now_used=Groups.objects.get(pk=pk)
    group_now_used.now_used=True #  изменяем поле now_used=True именно в том экземпляре Group, кот. сейчас используется 
    group_now_used.save() 
    return HttpResponseRedirect (reverse('edit_group', kwargs={'pk':pk} ) ) 
 

class Edit_Group(UpdateView):
    form_class = Edit_Group_Form 
    model = Groups
    template_name = 'edit_group.html'

    def form_valid(self, form):    
        c_d_f = form.cleaned_data                                           
        group=Groups.objects.get(pk=self.kwargs['pk']) # находим группу, которую редактируем
        group.group_name=c_d_f['group_name'] 
        group.headman=c_d_f['headman'] 
        group.save()
        return HttpResponseRedirect (reverse('students_list', kwargs={'pk_group':self.kwargs['pk']})) 

    def get_context_data(self, **kwargs):
        group=Groups.objects.get(pk=self.kwargs['pk'])
        context = super(Edit_Group, self).get_context_data(**kwargs)
        context['group']=group   
        context['group_students'] =group.students_set.all()     
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Edit_Group, self).dispatch(*args, **kwargs) 
           
def del_group(request,pk_group):
    del_g=Groups.objects.get(pk=pk_group)
    del_g.delete()
    return HttpResponseRedirect(reverse('groups_list'))                  

        
class Students_List(ListView):            
    template_name='students_list.html'
    context_object_name = 'students_list'
    
    def get_queryset(self):
        gr=Groups.objects.get(pk=self.kwargs['pk_group'])
        return gr.students_set.all( ) 

    def get_context_data(self, **kwargs):
        gr=Groups.objects.get(pk=self.kwargs['pk_group'])
        headman_id=gr.students_set.get(full_name=gr.headman)
        gr_count=gr.students_set.count
        context = super(Students_List, self).get_context_data(**kwargs)
        context['group'] = Groups.objects.get(pk=self.kwargs['pk_group'])
        context['group_all']= Groups.objects.all()
        context['headman_id']=headman_id.id        
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Students_List, self).dispatch(*args, **kwargs)
                    
class Add_Student(CreateView):
    form_class =Student_Form  
    template_name = 'add_student.html'
    
    def form_valid(self, form):    
        c_d_f = form.cleaned_data                                           
        Students.objects.create(**c_d_f)# создаем нового студента        
        st=Students.objects.get(full_name=c_d_f['full_name'])#вызываем его
        group=Groups.objects.get(pk=st.group_id )# вызываем его группу        
        group_students_set =group.students_set.all() # вызывыем всех студентов из его группы
        list_students=[e.id for e in group_students_set] # список id студентов
        if len(list_students) == 1:# если в этой группе он единственный студент
            group.headman_id=st.id   # делаем этого нового студента старостой
            group.save()
            return HttpResponseRedirect (reverse('students_list', kwargs={'pk_group':group.id}))
        else:
            # если это не ед. студент --старосту не меняем                 
            return HttpResponseRedirect (reverse('students_list', kwargs={'pk_group':group.id}))   
                    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Add_Student, self).dispatch(*args, **kwargs)     
 
 
def now_used_headman(requst,pk,pk_group_edit):
    group=Groups.objects.get(id=pk_group_edit)    
    if int(pk)==group.headman_id: #если студент-староста этой группы
        return HttpResponseRedirect (reverse('edit_headman', kwargs={'pk_group_edit':pk_group_edit,'pk':pk}))#то будем использовать класс Edit_Headman
    else: #если студент- не староста этой группы
        return HttpResponseRedirect (reverse('edit_student', kwargs={'pk_group_edit':pk_group_edit,'pk':pk}))#то будем использовать класс Edit_Student
 

class Edit_Headman(UpdateView):
                             
    form_class = Edit_Student_Form 
    model = Students
    template_name = 'edit_headman.html'

    def form_valid(self, form):
        c_d_f = form.cleaned_data        
        ed_hd=Students.objects.get(id=self.kwargs['pk'])
        ed_hd.full_name=c_d_f['full_name']
        ed_hd.date_of_birth=c_d_f['date_of_birth']
        ed_hd.student_id_number=c_d_f['student_id_number']        
        group=Groups.objects.get(pk=self.kwargs['pk_group_edit'])
        ed_hd.group_id=group.id        
        ed_hd.save() 
        return HttpResponseRedirect (reverse('students_list', kwargs={'pk_group': self.kwargs['pk_group_edit']}))
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Edit_Headman, self).dispatch(*args, **kwargs)            
      
class Edit_Student(UpdateView):
    form_class = Student_Form 
    model = Students
    template_name = 'edit_student.html'
   
    def form_valid(self, form):
        c_d_f = form.cleaned_data        
        ed_st=Students.objects.get(id=self.kwargs['pk'])
        ed_st.full_name=c_d_f['full_name']
        ed_st.date_of_birth=c_d_f['date_of_birth']
        ed_st.student_id_number=c_d_f['student_id_number']
        ed_st.group=c_d_f['group']
        ed_st.save() 
        return HttpResponseRedirect (reverse('students_list', kwargs={'pk_group': self.kwargs['pk_group_edit']}))
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Edit_Student, self).dispatch(*args, **kwargs)            


def del_student(request,pk_student,pk_group_del):
    st_del=Students.objects.get(pk=pk_student)
    st_del.delete()
    return HttpResponseRedirect (reverse('students_list', kwargs={'pk_group':pk_group_del} ))  
        
class Settings_List(TemplateView):
    template_name = "settings_list.html"
 
    




        
