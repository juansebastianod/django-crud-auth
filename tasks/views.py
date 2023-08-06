from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    
    user1=User.objects.values()
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'user':user1
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            print(request.POST['password1'])
            print(request.POST['password2'])
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])

                user.save()
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'user'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'ya existe chamo'
        })
        
@login_required
def tasks(request):
    
    tasks=Task.objects.filter(user=request.user,daracompleted__isnull=True)
    
    print(tasks)
    return render(request,'task.html',{
        'tasks':tasks
        
    })
    
@login_required
def tasks_completed(request):
    
    tasks=Task.objects.filter(user=request.user,daracompleted__isnull=False).order_by('title')
    
    print(tasks)
    return render(request,'task.html',{
        'tasks':tasks
        
    })
    
    
@login_required
def singout(request):
    logout(request)
    return redirect('home')


def signin(request):
    
    if request.method=="GET":
        return render(request,'signin.html',{
            'form':AuthenticationForm
        })
    else:
        user=authenticate(request,username=request.POST['username'],
                     password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
            'form':AuthenticationForm,
            'error':'username is incorrecr'
        })
        else:
            login(request,user)
            return redirect('tasks')
@login_required        
def create_task(request):
    
    if request.method=='GET':
        return render(request,'create_task.html',{
            
            'form':TaskForm
        })
    else:
        
        try:
            form=TaskForm(request.POST)
            new_task=form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request,'create_task.html',{
                'form':TaskForm,
                'error':'please provide valide data'
            })
@login_required            
def task_detail(request,task_id):
    if request.method=='GET':
        #task=Task.objects.get(pk=task_id)
        task=get_object_or_404(Task,pk=task_id,user=request.user)
        form =TaskForm(instance=task)
        return render(request,'task_detail.html',{
        'task':task,
        'form':form
        }
    )
    else:
        task=get_object_or_404(Task,pk=task_id,user=request.user)
        form=TaskForm(request.POST,instance=task)
        form.save()
        return redirect('tasks')
@login_required
def complete(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method=='POST':
        task.daracompleted=timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
        
    
        
                
        