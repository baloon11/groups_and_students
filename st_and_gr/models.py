# coding: utf-8
from django.db import models
from django.forms import ModelForm
from django.db.models.signals import post_init, post_save, post_delete
from django.dispatch import receiver
from datetime import datetime

class Info_About_Models(models.Model):  
    model_name=models.CharField(max_length=255,verbose_name=u'Имя модели')
    model_create=models.CharField(max_length=255,verbose_name=u'Информация о создании новой записи в модель')
    model_editing=models.CharField(max_length=255,verbose_name=u'Информация о редактировании модели')  
    model_delete=models.CharField(max_length=255,verbose_name=u'Информация об удалении записи из модели')
    class Meta:
        verbose_name_plural = "Информация о моделях"

    def __unicode__(self):
        return self.model_name 
       
class Students(models.Model):
    full_name = models.CharField(max_length=300, verbose_name=u'Полное имя')
    date_of_birth = models.CharField(max_length=300,verbose_name=u'Дата рождения')
    student_id_number=models.IntegerField(default=0,verbose_name=u'Номер студ. билета ')
    group=models.ForeignKey('Groups',verbose_name=u'Группа, к которой прикреплен студент')
    class Meta:
        verbose_name_plural = "Студенты"
        
    def __unicode__(self):
        return self.full_name
        
class Groups(models.Model):
    group_name=models.CharField(max_length=300,verbose_name=u'Название группы')
    headman=models.ForeignKey(Students,verbose_name=u'Староста')  
    now_used=models.BooleanField(default=False) #поле используется при редактировании группы(инф.о том, какая группа сейчас редактируется)
 
    class Meta:
        verbose_name_plural = "Группы"

    def __unicode__(self):
        return self.group_name    

@receiver(post_init, sender = Students) # создание новой записи (модель Students)
def post_init_students(instance, **kwargs):
    i_a_m=Info_About_Models.objects.get(model_name='Students') 
    i_a_m.model_create=datetime.now()
    i_a_m.save()

@receiver(post_save, sender = Students) # редактирование записи (модель Students)
def post_save_students(instance, **kwargs):
    i_a_m=Info_About_Models.objects.get(model_name='Students') 
    i_a_m.model_editing=datetime.now()
    i_a_m.save()

@receiver(post_delete, sender = Students) #  удаление записи (модель Students)
def post_delete_students(instance, **kwargs):
    i_a_m=Info_About_Models.objects.get(model_name='Students') 
    i_a_m.model_delete=datetime.now()
    i_a_m.save()

@receiver(post_init, sender = Groups) # создание новой записи (модель Groups)
def post_init_groups(instance, **kwargs):
    i_a_m=Info_About_Models.objects.get(model_name='Groups') 
    i_a_m.model_create=datetime.now()
    i_a_m.save()

@receiver(post_save, sender = Groups) # редактирование записи (модель Groups)
def post_save_groups(instance, **kwargs):
    i_a_m=Info_About_Models.objects.get(model_name='Groups') 
    i_a_m.model_editing=datetime.now()
    i_a_m.save()

@receiver(post_delete, sender = Groups) # удаление записи (модель Groups)
def post_delete_groups(instance, **kwargs):
    i_a_m=Info_About_Models.objects.get(model_name='Groups') 
    i_a_m.model_delete=datetime.now()
    i_a_m.save()
    
       

    