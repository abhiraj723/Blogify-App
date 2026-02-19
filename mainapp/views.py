from django.shortcuts import render, redirect
from mainapp.models import *
from django.contrib import messages
from mainapp.forms import Blogform

# Create your views here.

def index(request):
    blog = Blog.objects.all().order_by('-published_at')
    return render(request, 'index.html',{'blogs':blog})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            users = LoginInfo.objects.get(user=username, password=password)
            if users:
                request.session['adminid'] = users.user
                messages.success(request, 'Logged In Successfully')
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect('login')           
    return render(request, 'login.html')

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

def readblog(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'readblog.html', {'blogs':blog})

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