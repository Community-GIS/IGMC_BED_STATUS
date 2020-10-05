from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import bulkreg  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,auth
from .models import coordinat_up,doctor_up,formupdate, Coordinators, WardDetails,UserProfile, bulk_reg
from .resources import bulkResource
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,unauthenticated_user
from django.core.files.storage import FileSystemStorage
from tablib import Dataset
from django.http import JsonResponse
import openpyxl
from django.core.mail import send_mail

from django.http import HttpResponse


# Create your views here.

def healthDash(request):
    # context = {'site_url':settings.MY_SITE_URL}
    return render(request,"bed_dash/base.html")


def register(request):
    if request.method== "POST":
        username = request.POST['username']
        email = request.POST['email']
        # contact = request.POST['contact']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                print('Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                print('email taken')
                messages.info(request,"Email address Taken")
                return redirect('register')

            else:
                user = User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                messages.info(request,"User created")
                print('user created')
                return redirect('login')


        else:
            messages.info(request,"password does not match")

            print('password does not match.')
            return redirect('register')
        return redirect('xyz')

    else:
        return render(request, "bed_dash/register.html")

def role_reg(request):
    return render(request, 'bed_dash/role_register.html')

def last_up(request):
    return render(request, 'bed_dash/lastupdate.html')


# def assign_role(request):
#     if bulk_reg.objects.get(roles = 'admin') is True:
#         new_group, created = Group.objects.get_or_create(name ='admin') 
  
# # Code to add permission to group 
#         ct = ContentType.objects.get_for_model(User) 
    
# If I want to add 'Can go Haridwar' permission to level0 ? 
        # permission = Permission.objects.create(codename ='can_go_haridwar', 
        #                                 name ='Can go to Haridwar', 
        #                                         content_type = ct) 
        # new_group.permissions.add(permission)

def login(request):
    if request.method== "POST":
        username=request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(password=password,username=username)
        selected_field = username
        print(selected_field)
        if user is not None:
            data=bulk_reg.objects.get(name=selected_field);
            print(data.designation)
            role =data.designation
            # print(jsondata)
                # print(jsondata.designation)
            if role == 'admin':
                auth.login(request,user)
                return redirect("after_admin")
            elif role =='custodian':
                auth.login(request,user)
                return redirect("after_admin")
            elif role =='observer':
                auth.login(request,user)
                return redirect('observer')
            elif role =='coordinator':
                auth.login(request,user)
                return redirect("updatecoord")
            elif role =='doctor':
                auth.login(request,user)
                return redirect("updatedoc")
            elif role =='opd coordinator':
                auth.login(request,user)
                return redirect("after_admin")
            # auth.login(request,user)
            # return redirect('role_register')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'bed_dash/login.html')

@login_required(login_url="login")
def xyz(request):
    return render(request, 'bed_dash/health.html')

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def coord(request):
    if request.method =="POST":
        date = request.POST.get('date')
        cordname = request.POST.get('cordname')
        contnum = request.POST.get('contnum')
        altnum =request.POST.get('altnum')
        schfrom = request.POST.get('from')
        schto = request.POST.get('to')
        
        sub= coordinat_up(date=date,cordname=cordname,contnum=contnum,altnum=altnum,schfrom=schfrom,schto=schto )
        # if new_form.is_valid():
        #     new_form.save() 
        sub.save()
        print('submitted')
        return redirect('/')
    else:
        return render(request, 'bed_dash/coordinator.html')
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def doc(request):
    if request.method =="POST":
        date = request.POST.get('date')
        docname = request.POST.get('docname')
        contnum = request.POST.get('contnum')
        altnum =request.POST.get('altnum')
        schfrom = request.POST.get('from')
        schto = request.POST.get('to')
        
        sub=doctor_up(date=date,docname=docname,contnum=contnum,altnum=altnum,schfrom=schfrom,schto=schto )
        # if new_form.is_valid():
        #     new_form.save() 
        sub.save()
        print('submitted')
        return redirect('/')
    else:
        return render(request, 'bed_dash/doctor.html')# def UrbanHealth(request):


@login_required(login_url="login")
# @allowed_users(allowed_roles=['admin'])
def ad(request):
    data = coordinat_up.objects.all()
    docdata  = doctor_up.objects.all()
    upform= formupdate.objects.all()
    time= formupdate.objects.values('tme')
    x = time
    print(x)
    return render(request,"bed_dash/admin.html",{"data":data,"docdata":docdata,"upform":upform,"time":time})
@login_required(login_url="login")
# @allowed_users(allowed_roles=['admin'])

def update_coord(request):
    

    if request.is_ajax():
        selected_field = request.GET['name']
        docinfo = list(Coordinators.objects.filter(name=selected_field).values());
        # print(docinfo[0]["unit"])
        field = docinfo[0]["unit"]
        wardinfo = list(WardDetails.objects.filter(unit=field).values()); 
        # print(wardinfo)
        jsondata =docinfo[0]
        # print(jsondata)
        jsondata1= wardinfo[0]
        # print(jsondata1)
        data = {'jsondata': jsondata, 'jsondata1': jsondata1}

        # merged_dict = {key: value for (key, value) in (jsondata.items() + jsondata1.items())}
        print(data)
        return JsonResponse(data)
    if request.method=="POST":
        date = request.POST.get('date')
        tme=request.POST.get('tme')
        upby=request.POST.get('upby')
        contnum=request.POST.get('contnum')
        wardnum = request.POST.get('wardnum')
        wardtype = request.POST.get('wardtype')
        vacbed =request.POST.get('vacbed')
        ventbed =request.POST.get('ventbed')
        oxybed = request.POST.get('oxybed')
        
        sub=formupdate(date=date,vacbed=vacbed,wardnum=wardnum,tme= tme,wardtype=wardtype,ventbed=ventbed,oxybed=oxybed,upby=upby,contnum=contnum)
        # if new_form.is_valid():
        #     new_form.save() 
        sub.save()
        print('submitted')
        return render(request, 'bed_dash/whatsapp.html')
    else:
        cordname= Coordinators.objects.all()
        wardetail= WardDetails.objects.all()
        queryset=formupdate.objects.all()
        # form=queryset.reverse()[0]
        # print(cordname)
        return render(request, 'bed_dash/update_bed.html',{"cordname":cordname,"wardetail":wardetail})

def update_doc(request):
    if request.is_ajax():
        selected_field = request.GET['name']
        docinfo = list(Coordinators.objects.filter(name=selected_field).values()); 
        jsondata =docinfo[0]
        return JsonResponse(jsondata)
    if request.method=="POST":
        date = request.POST.get('date')
        tme=request.POST.get('tme')
        upby=request.POST.get('upby')
        contnum=request.POST.get('contnum')
        wardnum = request.POST.get('wardnum')
        wardtype = request.POST.get('wardtype')
        vacbed =request.POST.get('vacbed')
        ventbed =request.POST.get('ventbed')
        oxybed = request.POST.get('oxybed')
        
        sub=formupdate(date=date,vacbed=vacbed,wardnum=wardnum,tme= tme,wardtype=wardtype,ventbed=ventbed,oxybed=oxybed,upby=upby,contnum=contnum)
        # if new_form.is_valid():
        #     new_form.save() 
        sub.save()
        print('submitted')
        return render(request, 'bed_dash/whatsapp.html')
    else:
        cordname= Coordinators.objects.all()
        wardetail= WardDetails.objects.all()
        # print(cordname)
        return render(request, 'bed_dash/doc_update.html')

def role_coord(request):
    return redirect("updatecoord")

def role_doc(request):
    return redirect("updatedoc")

def obsrvr(request):
    data = coordinat_up.objects.all()
    docdata  = doctor_up.objects.all()
    upform= formupdate.objects.all()
    time= formupdate.objects.values('tme')
    x = time
    print(x)
    return render(request,"bed_dash/observer.html",{"data":data,"docdata":docdata,"upform":upform,"time":time})
    # return render(request,"bed_dash/observer.html")


def upload(request):
    if request.method == 'POST':
        context = {}
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        return render(request, 'bed_dash/upload.html', context)
    else:
        return render(request, 'bed_dash/upload.html')


def show(request):  
    datas = bulk_reg.objects.all()
    print(datas)
    # docdata  = doctor.objects.all()
    # upform= formupdate.objects.all()
    # time= formupdate.objects.values('tme')
    # x = time
    # print(x)
    return render(request,"bed_dash/admin.html",{"datas":datas})
    
def edit(request, id):  
    data = bulk_reg.objects.get(id=id)
    # docdata  = doctor.objects.get(id=id)  
    return render(request,'bed_dash/edit.html', {'data':data})  
def update(request, id):
    data = bulk_reg.objects.get(id=id) 
    print(data) 
    form = bulkreg(request.POST, instance = data)  
    print(form)
    if form.is_valid(): 
        print("success") 
        form.save()  
        return redirect("/show/")  
    else:
        print("fail")
    return render(request, 'bed_dash/edit.html', {'data': data}) 


def destroy(request, id):  
    data = bulk_reg.objects.get(id=id)  
    data.delete()  
    return redirect("/show/")  

def simple_upload(request):
    if request.method== "POST":
        bulk_resource = bulkResource()
        dataset = Dataset()
        bulk =request.FILES['myFile']
        print(bulk)
        if not bulk.name.endswith('xlsx'):
            messages.info(request,'wrong format')
            return render(request, "bed_dash/upload.html")

        imported_data = dataset.load(bulk.read(),format='xlsx')
        print(imported_data)
        for data in imported_data:
            value = bulk_reg(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4]                        ,
                    data[5],
                    data[6],
                    data[7]
                    )
            # print(value)
            # value.save()
            # bulkdata=bulk_reg.objects.all()

            if bulk_reg.objects.filter(name=data[1]).exists():
                # databulk= bulk_reg.objects.all()
                print(data[1])
                messages.info(request,"Name already entered")
                # return render(request, "bed_dash/upload.html")
            else:
                value.save()
                messages.info(request,"datas entered")

                # return render(request, "bed_dash/upload.html")
        
                

            # else:
            #     value.save()
            #     print(value)
            #     messages.info(request,"data entered")
            #     return render(request,"bed_dash/upload.html")
        data_bulk=bulk_reg.objects.all()
        print(data_bulk) 
        for i in data_bulk:
            username = i.name
            email = i.email
                        # contact = request.POST['contact']
            password = i.mobile
                            # password2 = request.POST['password2']
                            # if password1 == password2:
            if User.objects.filter(username=username).exists():
                    messages.info(request,"Username Taken")
                    print('Username taken')
                    # return render(request,"bed_dash/upload.html")
            elif User.objects.filter(email=email).exists():
                    print('email taken')
                    messages.info(request,"Email address Taken")
                    # return render(request,"bed_dash/upload.html")

            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                messages.info(request,"User created")
                print('user created')
               
                stuff_in_string = "Hello {} Your username is {} and Password is {}.Thanks!!".format(username,username, password)
                print(stuff_in_string)
                # email=i.email }}
                send_mail('IGMC', stuff_in_string, 'igmchospitalnagpur@gmail.com',
                    [i.email], fail_silently=False)        
        return render(request,"bed_dash/upload.html")
            

    else:
        return render(request,"bed_dash/upload.html")
def emp(request):  
    if request.method == "POST":  
        form = bulkreg(request.POST) 
        print(form)
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('show')  
            except:  
                pass  
    else:  
        form = bulkreg()
        print(form)  
    return render(request,'bed_dash/bulk.html',{'form':form})  

def adafter(request):
    return render(request,'bed_dash/afteradmin.html')  


def ward(request):
    if request.is_ajax():
        selected_field = request.GET['name']
        docinfo = list(Coordinators.objects.filter(name=selected_field).values()); 
        jsondata =docinfo[0]
        return JsonResponse(jsondata)