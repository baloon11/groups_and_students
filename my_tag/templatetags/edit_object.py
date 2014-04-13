from django import template
from django.contrib.auth.models import User
"""
This tag returns a link to the edit page (in the admin panel) of the specified object.
   Usage(examples)
   
{% edit obj='Students' %}  -- Link to edit the object 'Students' (all list). 
{% edit obj='Students' obj_id=2 %} -- Link to edit an instance (model 'Students', id=2).
{% edit user=request.user obj_id=1 %} -- Link to edit the current user (with id).
{% edit user=request.user %} -- Link to edit the current user ( without id ).

{% edit user=request.user obj_id=2 %} -- Mistake. Arguments 'user' and 'obj_id' are not from the same user (request.user has id=1). 
{% edit user=request.user obj='Students' %} -- Mistake. You entered more than one object. 
{% edit user=request.user obj='Students' obj_id=2 %} -- Mistake. You have entered too many parameters. 
"""

register = template.Library()
@register.simple_tag 
def edit(obj='',obj_id=0,user=''):
    link=''
    if user=="all_users" and obj==False and obj_id==False: 
        link='<a href="/admin/auth/user/">all_users</a>'
           
    if user and obj_id: 
        search_user_username=User.objects.get(username=user)
        search_user_id=User.objects.get(id=obj_id)
        if search_user_username==search_user_id: #when the arguments 'user' and 'obj_id' refer to a single user                
            link='<a href="/admin/auth/user/'+str(obj_id)+'/">'+str(user)+'</a>'#return a link to the edit page 
        else: 
            link='arguments \'user\' and \'obj_id\' are not from the same user'
       
    if  user and obj_id==False:
        search_user_username=User.objects.get(username=user)        
        str_user_id=str(search_user_username.id)
        link='<a href="/admin/auth/user/'+str_user_id+'/">'+str(user)+'</a>'
        
    if obj and obj_id:
        obj_lower=obj.lower()
        link='<a href="/admin/st_and_gr/'+obj_lower+'/'+str(obj_id)+'/">'+obj+'/'+str(obj_id)+'/</a>'        
    elif obj and obj_id==False:   
        obj_lower=obj.lower()
        link='<a href="/admin/st_and_gr/'+obj_lower+'/">'+obj+'</a>'        

    if user and obj:
        link="You entered more than one object"

    if obj_id and user and obj:
        link="You have entered too many parameters"

    return link    