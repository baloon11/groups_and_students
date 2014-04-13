from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from st_and_gr.views import Start,Registration,Groups_List,Create_Group,Edit_Group,Students_List,Add_Student,Edit_Student,Settings_List,now_used_group,Edit_Headman,now_used_headman

from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
     
     url(r'^$',Start.as_view(), name='start'),
     url(r'^registration/$',Registration.as_view(), name='registration'),
     url(r'^settings_list/$',Settings_List.as_view(), name='settings_list'),
     url(r'^logout/$','st_and_gr.views.logout', name='logout'),
#________________________________
     url(r'^groups_list/$',Groups_List.as_view(), name='groups_list'),     
     url(r'^group/create/$',Create_Group.as_view(), name='create_group'),
     url(r'^group/(?P<pk>\d+)/now_used_group/$','st_and_gr.views.now_used_group', name='now_used_group'),
     url(r'^group/(?P<pk>\d+)/edit/$',Edit_Group.as_view(), name='edit_group'),
     url(r'^group/(?P<pk_group>\d+)/del/$','st_and_gr.views.del_group', name='del_group'),
#________________________________     
     url(r'^list_of_students_for_the_group/(?P<pk_group>\d+)/$', Students_List.as_view(), name='students_list'),
     url(r'^student/add/$',Add_Student.as_view(), name='add_student'),
     
     url(r'^student/(?P<pk>\d+)/group/(?P<pk_group_edit>\d+)/now_used_headman/$','st_and_gr.views.now_used_headman', name='now_used_headman'),
     url(r'^headman/(?P<pk>\d+)/group/(?P<pk_group_edit>\d+)/edit/$', Edit_Headman.as_view(), name='edit_headman'),
     url(r'^student/(?P<pk>\d+)/group/(?P<pk_group_edit>\d+)/edit/$', Edit_Student.as_view(), name='edit_student'),
      
     url(r'^student/(?P<pk_student>\d+)/group/(?P<pk_group_del>\d+)/del/$','st_and_gr.views.del_student', name='del_student'),
#________________________________      
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
     url(r'^admin/', include(admin.site.urls))
                       )
if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
