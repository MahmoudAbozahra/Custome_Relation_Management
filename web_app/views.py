from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib.auth import authenticate ,login ,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import logging
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request , 'web/index.html')


def register(request):
    form = CreateUserForm  #object from class Createuserform
    if request.method == 'POST':  #check request GET or POST
        form=CreateUserForm(request.POST)  #put request data in form
        if form.is_valid:     #check the data in form is vaild 
            form.save()  #save data
            messages.success(request,'Register is successfuly!')
            return redirect('my_login')
    else:
        form = CreateUserForm()   #if request not post show a form only
    
    context = {'form':form}  #Dictionary that retrieves and display the data in html page
    
    return render(request, 'web/register.html',context) #return request to display the the html page



#login user
def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form=LoginForm(request , data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user = authenticate(request , username=username , password=password)
            
            if user is not None:
                login(request,user)
                messages.success(request,'Login successfuly!')
                return redirect('dashboard')
        else:
            form=LoginForm()
        
    context={'form':form}
        
    return render(request, 'web/login.html' ,context)



def my_logout(request):
    logout(request)
    messages.success(request,'Logout successfuly!')
    return redirect('my_login')
    
    
@login_required(login_url='my_login')
def dashboard(request):
    clints = Clint.objects.all()
    form = ClintForm()
    context = {
        'clints': clints,
        'form': form,
    }
    return render(request, 'web/dashboard.html', context)
                
        
        
@login_required(login_url='my_login')              
def add_clint(request):
    form = ClintForm()
    if request.method == 'POST':
        form = ClintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Clint added successfuly!')
            return redirect('dashboard')
    else:
        form = ClintForm()
        
    return render(request , 'web/add_clint.html',{'form':form})


@login_required(login_url='my_login')
def delete(request,id):
    clint = get_object_or_404(Clint,id=id)
    clint.delete()
    messages.success(request,'Clint deleted successfuly!')
    return redirect('dashboard')
    


def view(request,id):
    clint = get_object_or_404(Clint , id=id)
    
    
    return render(request,'web/view.html', {'clint': clint})

@login_required(login_url='my_login')
def edit(request,id):
    clint = get_object_or_404(Clint , id=id)
    if request.method == 'POST':
        clint_update = ClintForm(request.POST , instance=clint)
        if clint_update.is_valid():
            clint_update.save()
            return redirect('dashboard')
    else:
        clint_update=ClintForm(instance=clint)
        
        
    
    return render(request,'web/edit.html', {'form': clint_update})

from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def search(request):
    query = request.GET.get('query')
    results = []
    try:
        if query:
            results = Clint.objects.filter(
                Q(first_name__icontains=query) | Q(id__icontains=query)
            )
    except Exception as e:
        logger.error('Error during search: %s', e)
        
    return render(request, 'web/search.html', {'results': results, 'query': query})



def custom_page_not_found(request, exception):
    return render(request, 'web/404.html', status=404)