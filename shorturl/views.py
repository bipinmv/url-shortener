from django.shortcuts import render,redirect,get_object_or_404
from .models import Url
from .forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import string
import random
# Create your views here.

def index(request):
    return render(request,'index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            user_form=UserForm(request.POST)

            if user_form.is_valid():
                user=user_form.save()
                user.set_password(user.password)
                user.save()
                messages.success(request,"Account created successfully")
                return redirect('login')
            else:
                print(user_form.errors)
        else:
            user_form=UserForm()       
        return render(request,'signup.html',{'user_form':user_form}) 

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user=authenticate(request,username=username,password=password)
            if user:
                if user.is_superuser:
                    login(request,user)
                    return redirect('admin:index')
                elif user.is_active:
                    login(request,user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:    
                        return redirect('index')
            else:
                messages.error(request,'Invalid credential')

        return render(request,'login.html')     

@login_required(login_url='login')
def userlogout(request):
    logout(request)
    return redirect('index')   

@login_required(login_url='login')
def dashboard(request):
    result=Url.objects.filter(user=request.user).order_by('id').reverse()
    return render(request,'profile.html',{'result':result})

def external(request,surl):
    # short=get_object_or_404(Url,id=id)
    short=Url.objects.get(urlkey=surl)
    return redirect(short.url)

def shorten(request):
    urlinput=request.POST.get('urlinput')
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_key=''.join(random.choice(chars) for _ in range(6))
    surl="https://bitly.com/" + random_key
    keycheck=Url.objects.filter(urlkey=random_key)
    if request.user.is_authenticated:
        if request.method=='POST':
            if keycheck.count()==0:
                feed=Url.objects.create(user=request.user,url=urlinput,shorturl=surl,urlkey=random_key)
                return redirect('dashboard')
            else:    
                return redirect('index')
        return redirect('index')   
    else:
        if request.method=='POST':
            if keycheck.count()==0:
                feed=Url.objects.create(url=urlinput,shorturl=surl,urlkey=random_key)
                #unauthurl=Url.objects.filter(url=urlinput)
                #return HttpResponseRedirect(reverse('index', kwargs={'unauthurl':unauthurl}))
                #return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                return render(request,'index.html',{'longurl':urlinput,'shorturl':surl})
            else:    
                return redirect('index')
        return redirect('index')  
        
     