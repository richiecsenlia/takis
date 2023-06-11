from django.shortcuts import render
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required

from accounts.models import TeachingAssistantProfile, MataKuliah
from authentication.forms import UserCreateForm, PasswordForm

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
    login_check = login_required(login_url=reverse_lazy('authentication:login'))
    role_test = user_passes_test(ta_role_check)
    return login_check(role_test(function))

def admin_required(function):
    login_check = login_required(login_url=reverse_lazy('authentication:login'))
    role_test = user_passes_test(admin_role_check)
    return login_check(role_test(function))

def login_handler(request):
    error = None
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('main:homepage'))
    if request.method == "POST" :
        data = request.POST
        user = authenticate(username=data['username'],password=data['password'])
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(request.GET.get('next','/'))
        error = 'username / password tidak sesuai'
    response = {'error' : error}
    return render(request,'registration/login.html',response)

def register(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('main:homepage'))
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
    form = PasswordForm()
    if request.method == "POST":
        form = PasswordForm(request.POST)
        if (form.is_valid()):
            user = request.user
            user.set_password(request.POST['password1'])
            user.save()
            user = authenticate(username=user.username,password=user.password)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse('main:homepage'))
    response={'form':form}
    return render(request,'registration/change_password.html',response)

def not_assign(request):
    response = {}
    return render(request,'registration/not_assign.html',response)

def exclude_matkul(filter_matkul,users,matkul_choices):
    if len(filter_matkul) != 0:
        for matkul in matkul_choices:
            if not (matkul.nama in filter_matkul):
                users = users.exclude(teachingassistantprofile__daftar_matkul__id = matkul.id)
    return users
def exclude_kontrak(filter_kontrak,users,kontrak_choices):
    if(len(filter_kontrak) != 0) :
        for kontrak in kontrak_choices :
            if not (kontrak[1] in filter_kontrak):
                users = users.exclude(teachingassistantprofile__kontrak = kontrak[1])
    return users
def exclude_status(filter_status,users,status_choices):
    if len(filter_status) !=0 :
        for status in status_choices :
            if not (status[1] in filter_status):
                users = users.exclude(teachingassistantprofile__status= status[1])
    return users
def exclude_prodi(filter_prodi,users,prodi_choices):
    if len(filter_prodi) != 0 :
        for prodi in prodi_choices :
            if not (prodi[1] in filter_prodi):
                users = users.exclude(teachingassistantprofile__prodi = prodi[1])
    return users
def change_role(request):
    users = User.objects.all()
    filter_kontrak = request.GET.getlist("kontrak")
    filter_status = request.GET.getlist("status")
    filter_prodi = request.GET.getlist("prodi")
    filter_matkul = request.GET.getlist("matkul")
    kontrak_choices = TeachingAssistantProfile.kontrak.field.choices
    status_choices = TeachingAssistantProfile.status.field.choices
    prodi_choices = TeachingAssistantProfile.prodi.field.choices
    matkul_choices = MataKuliah.objects.order_by('nama')

    users = exclude_kontrak(filter_kontrak,users,kontrak_choices)
    users = exclude_status(filter_status,users,status_choices)
    users = exclude_prodi(filter_prodi,users,prodi_choices)
    users = exclude_matkul(filter_matkul,users,matkul_choices)
    
    response = {'users':users,
        'kontrak_choices': kontrak_choices,
        'status_choices': status_choices,
        'prodi_choices': prodi_choices,
        'matkul_choices': matkul_choices,
        'filter_kontrak':filter_kontrak,
        'filter_status':filter_status,
        'filter_prodi':filter_prodi,
        'filter_matkul':filter_matkul,
    }
    
    return render(request, 'registration/change_role.html',response)

def update_role(request,id,role):
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        return HttpResponse("user tidak ditemukan")
    user.role.role = role
    user.role.save()
    return HttpResponseRedirect(reverse('authentication:change_role'))

