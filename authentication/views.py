from django.shortcuts import render
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from .forms import UserForm,UserCreateForm,PasswordForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required

# Create your views here.



def ta_role_check(user):
    if str(user.role) == 'TA':
        return True
    else:
        raise PermissionDenied
    
def admin_role_check(user):
    if str(user.role) == 'admin':
        return True
    else:
        raise PermissionDenied

def ta_required(function):
    login_check = login_required(login_url=reverse_lazy("authentication:login"))
    role_test = user_passes_test(ta_role_check)
    return login_check(role_test(function))

def admin_required(function):
    login_check = login_required(login_url=reverse_lazy("authentication:login"))
    role_test = user_passes_test(admin_role_check)
    return login_check(role_test(function))

def login_handler(request):
    if request.method == "POST" :
        data = request.POST
        user = authenticate(username=data['username'],password=data['password'])
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("main:homepage"))
    form = UserForm()
    response = {'form':form}
    return render(request,'registration/login.html',response)

def register(request):
    form = UserCreateForm()
    if request.method == "POST" :
        form = UserCreateForm(request.POST)
        if (form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('authentication:login'))
    response = {'form':form}
    return render(request,'registration/register.html',response)

def change_password(request):
    if not request.user.is_authenticated  :
        return HttpResponseRedirect(reverse('authentication:login'))
    if len(request.user.password) != 0:
        return HttpResponseRedirect(reverse("main:homepage"))
    form = PasswordForm()
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if (form.is_valid()):
            user = request.user
            user.set_password(request.POST['password'])
            user.save()
            user = authenticate(username=user.username,password=user.password)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse("main:homepage"))
    response={'form':form}
    return render(request,'registration/change_password.html',response)

def not_assign(request):
    response = {}
    return render(request,'registration/not_assign.html',response)

def change_role(request):
    users = User.objects.all()
    response = {'users':users}
    return render(request, 'registration/change_role.html',response)

def update_role(request,id,role):
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse("user tidak ditemukan")
    user.role.role = role
    user.role.save()
    return HttpResponseRedirect(reverse("authentication:change_role"))

