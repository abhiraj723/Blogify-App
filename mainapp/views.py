from django.shortcuts import render, redirect
from mainapp.models import *
from django.contrib import messages
from mainapp.forms import Blogform
from django.db import transaction

# Create your views here.

def index(request):
    userid = request.session.get('adminid') or request.session.get('readerid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(user=userid)
        if obj.usertype == "admin":
            user = obj
        if obj.usertype == "reader":
            user = Reader.objects.get(user=obj)
    blog = Blog.objects.all().order_by('-published_at')
    return render(request, 'index.html',{'blogs':blog,'user':user})

def login_view(request):
    userid = request.session.get('adminid') or request.session.get('readerid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(user=userid)
        if obj.usertype == "admin":
            user = obj
        if obj.usertype == "reader":
            user = Reader.objects.get(user=obj)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            users = LoginInfo.objects.get(user=username, password=password)
            if users and users.usertype == "admin":
                request.session['adminid'] = users.user
                request.session.set_expiry(0)
                messages.success(request, 'Logged In Successfully')
                return redirect('admindash')
            if users and users.usertype == "reader":
                request.session['readerid'] = users.user
                request.session.set_expiry(0)
                messages.success(request, 'Logged In Successfully')
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect('login')           
    return render(request, 'login.html',{'user':user})

def readerdash(request):
    if 'readerid' not in request.session:
        messages.error(request,"please login first")
        return redirect('login')
    userid = request.session.get('readerid')
    user = LoginInfo.objects.get(user=userid)
    reader = Reader.objects.get(user=user)
    return render(request,"readerdash.html",{'reader':reader})

def register(request):
    userid = request.session.get('adminid') or request.session.get('readerid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(user=userid)
        if obj.usertype == "admin":
            user = obj
        if obj.usertype == "reader":
            user = Reader.objects.get(user=obj)
    if request.method == "POST":
        usertype = request.POST.get('usertype')
        email = request.POST.get('email')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        exist = LoginInfo.objects.filter(user=email)
        if exist:
            messages.warning(request,'Email is already registered')
            return redirect('register')
        try:
            with transaction.atomic():
                log = LoginInfo(usertype=usertype,user=email,password=password)
                if usertype == "reader":
                    reader = Reader(user=log,name=name,gender=gender)
                    log.save()
                    reader.save()
                    messages.success(request, 'Register Successfully')
                    return redirect('login')
        except Exception as e:
            messages.error(request, "something went wrong")
            return redirect('register')           
    return render(request, 'register.html',{'user':user})

def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request, "Please Login First")
        return redirect('login')
    blog_count = Blog.objects.all().count()
    return render(request, 'admindash.html',{'blog_count':blog_count})

def addblog(request):
    if not 'adminid' in request.session:
        messages.error(request, "Please Login First")
        return redirect('login')
    form = Blogform()
    if request.method=="POST":
        form = Blogform(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, "Blogs Added Successfully")
            return redirect('addblog')
    return render(request, 'addblog.html',{'form':form})

def viewblog(request):
    if not 'adminid' in request.session:
        messages.error(request, "Please Login First")
        return redirect('login')
    bl = Blog.objects.all().order_by('-published_at')
    return render(request, 'viewblog.html',{'blogs':bl})

def logout_view(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, "Logged Out SuccessFully")
        return redirect('login')
    return redirect('login')

def readerlogout(request):
    if 'readerid' in request.session:
        del request.session['readerid']
        messages.success(request, "Logged Out SuccessFully")
        return redirect('login')

def readblog(request, id):
    if 'readerid' not in request.session:
        messages.error(request,"Login first to view full details.")
        return redirect('login')
    userid = request.session.get('adminid') or request.session.get('readerid')
    user = None
    if userid:
        obj = LoginInfo.objects.get(user=userid)
        if obj.usertype == "admin":
            user = obj
        if obj.usertype == "reader":
            user = Reader.objects.get(user=obj)
    

    blog = Blog.objects.get(id=id)
    return render(request, 'readblog.html', {'blogs':blog,'user':user})

def delete_blog(request, id):
    bl = Blog.objects.get(id=id)
    bl.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('viewblog')

def editblog(request,id):
    if not 'adminid' in request.session:
        messages.error(request, "Please Login First")
        return redirect('login')
    bl = Blog.objects.get(id=id)
    form = Blogform(instance=bl)
    if request.method=="POST":
        data = Blogform(request.POST, request.FILES, instance=bl)
        if data.is_valid:
            data.save()
            messages.success(request, "Blog Changes Successfully")
            return redirect('viewblog')
    return render(request, 'editblog.html',{'form':form})