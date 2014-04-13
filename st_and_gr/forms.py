# -*- coding: utf-8 -*-
from django import forms
from st_and_gr.models import Groups,Students,Info_About_Models
from django.contrib.auth.models import User

class Start_Form(forms.Form):
    username = forms.CharField(max_length=100,label='Логин/e-mail')
    password= forms.CharField( label='Пароль',widget=forms.PasswordInput())

class Reg_Form(forms.ModelForm):
    username = forms.CharField(label='Логин')
    email=forms.EmailField(label='e-mail')
    class Meta:
        model = User   
        fields = ('username','email','password')
        widgets = {'password':forms.PasswordInput()}

class Edit_Group_Form(forms.ModelForm):   
    class Meta:
        model = Groups
        fields = ('group_name','headman')

    def __init__(self, *args, **kwargs): 
        super(Edit_Group_Form, self).__init__(*args, **kwargs)
        gr=Groups.objects.get(now_used=True)
        students_set=gr.students_set.all()  
        self.fields['headman'].queryset=students_set # в выпадающем списке будут только студенты выбранной группы         
        
class Create_Group_Form(forms.ModelForm):   
    class Meta:
        model = Groups
        fields = ('group_name',)        
            
class Student_Form(forms.ModelForm):
    class Meta:
        model = Students      

class Edit_Student_Form(forms.ModelForm):
    class Meta:
        model = Students      
        fields = ('full_name','date_of_birth','student_id_number')

    
    
                       
  