from django.conf import settings
def my_vars(request):
    return {      
        'MY_SETTINGS': settings
           }