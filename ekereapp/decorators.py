from django.http import HttpResponse
from django.shortcuts import redirect



def authenticated_user(view_func):
    def verify_func(request,*args,**kwargs):

        if request.user.is_authenticated:
            return redirect('home')
            
        else:
            
            return view_func(request,*args,**kwargs)
    
    return verify_func


def allowed_user(view_func):
    def verify_func(request,*args,**kwargs):

        if request.user.is_authenticated:
            group=None
            if request.user.groups.exists():
                group=group=request.user.groups.all()[0].name
            if group=='admin':
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
            
        else:
            return redirect('home')
    
    return verify_func