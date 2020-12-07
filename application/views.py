from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from datetime import datetime
from datetime import time as dtime
from django.http import JsonResponse
import json

# this fuction takes form fields, validate them and save in job model
def createJob(request):
    if request.method == "POST":
        title           = request.POST['jobTitle']
        description     = request.POST['jobDescription']
        location        = request.POST['location']
        total_days      = request.POST['totalDays']
        hours_per_day   = request.POST['hoursPerDay']
        start_date      = request.POST['startDate']
        start_time      = request.POST['startTime']
        task_types      = request.POST['taskListInput']
        group_types     = request.POST['groupListInput']
        note            = ""
        if 'specialNote' in request.POST and request.POST['specialNote'] != "":
            note = request.POST['specialNote']

        print(title)
        print(description)
        print(location)
        print(total_days)
        print(hours_per_day)
        print(type(start_time))
        print(task_types)
        print(group_types)

        new_job = job(
            title = title,
            description = description,
            location = location,
            total_days = int(total_days),
            hours_per_day = int(hours_per_day),
            start_date = start_date,
            start_time = start_time,
            task_types = task_types,
            group_types = group_types,
            note = note,
            posted_by = request.user
        )

        new_job.save()


    return redirect("index")

def get_filtered_jobs(request, status):
    if status == "all":
        all_jobs = job.objects.all()
    else:
        all_jobs = job.objects.filter(status = status)

    if all_jobs.exists():
        if request.user.ifClient:
            all_jobs = all_jobs.filter(posted_by = request.user)

            print(len(all_jobs))
    return all_jobs

# main page function

def index(request):

    if not request.user.is_authenticated:
        return redirect("login")

    # if request.user.ifClient:
    #     if job.objects.filter(posted_by = request.user).exists():
    #         context["all_jobs"] = job.objects.filter(posted_by = request.user)

    # if request.user.ifFreelancer:
    #     if job.objects.filter(status = "Open").exists():
    #         context["all_jobs"] = job.objects.filter(status = "Open")
        
    return redirect("jobs")
    
    # return render(request, 'main.html')

# show jobs panel
def jobs(request):
    context = {}
    status = "all"

    if 'status' in request.GET and request.GET['status'] != "":
        status = request.GET['status']
   
    context['all_jobs'] = get_filtered_jobs(request, status)
    return render(request, 'main.html', context)

# function for signup
def register(request, type):
    if request.user.is_authenticated:
        return redirect("index")

    if type == "freelancer":
        LIST = [
            "Verpleegkunde MBO",
            "Verpleegkunde MBO 4",
            "Verzorgende IG",
            "Verzorgende AG",
            "Helpende Plus",
            "Helpende Plus",
            "Thuisbegeleider",
            "Social Work",
            "Social Pedagogische Werk",
            "Social Pedagogische Hulpverlening",
            "Pedagogisch medewerker kinderopvang",
            "Agogisch Medewerker",
            "Maatschappelijke Zorg",
            "Maatschappelijk Werk en Dienstverlening",
            "Persoonlijk begeleider specifieke doelgroepen",
            "Persoonlijk begeleider gehandicaptenzorg",
            "Other"
        ]
        return render(request, "signup.html", {'specialities': LIST})
    elif type == "client":
     
        return render(request, "client.html")
    else:
        return redirect("login")      

# function for login
def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }

        user = authenticate(username = email, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("index")
    
        messages.info(request, "Incorrect login details!")
        return render(request, "login.html", context)
            # return redirect("login")
    else:
        return render(request, "login.html")

# function for logout
def logout(request):
    auth.logout(request)
    return redirect("index")

# function to create client
def createClient(request):
    if request.method == "POST":
        information = {
            "organizationName":     request.POST.get("organizationName"),
            "kvkNumber":            request.POST.get("kvkNumber"),
            "email":                request.POST.get("email"),
            "phone":                request.POST.get("phone"),
            "firstName":            request.POST.get("firstName"),
            "lastName":             request.POST.get("lastName"),
            "homeAddress":          request.POST.get("homeAddress"),
            "addressNumber":        request.POST.get("addressNumber"),
            "postcode":             request.POST.get("postcode"),
            "city":                 request.POST.get("city"),
            "pass1":                request.POST.get("pass1"),
            "pass2":                request.POST.get("pass2")
        }

        if information['pass1'] != information['pass2']:
            information["border"] = "password"
            return render(request, "client.html", information)

        filteration = client.objects.all()

        if filteration.filter(email = information["email"]).exists():
            information["border"] = "email"
            return render(request, "client.html", information)

        # if filteration.filter(kvkNumber = information["kvkNumber"]).exists():
        #     information["border"] = "kvkNumber"
        #     return render(request, "client.html", information)

        newClient = client(
            organization_name   = information["organizationName"],
            kvkNumber           = information["kvkNumber"],
            email               = information["email"],
            phone               = information["phone"],
            firstName           = information["firstName"],
            lastName            = information["lastName"],
            homeAddress         = information["homeAddress"],
            addressNumber       = information["addressNumber"],
            postcode            = information["postcode"],
            city                = information["city"]
        )
        
        newClient.save()

        newUser = User.objects.create_user(username=information["email"], first_name=information["firstName"], password=information["pass1"], ifClient=newClient)
        newUser.save()

        for i, j in information.items():
            print(f'{i} => {j}')

        messages.info(request, "Your account has been created successfully!")

    return redirect("login")

# function to create freelancer
def createFreelancer(request):
    if request.method == "POST":
        information = {
            "firstName":        request.POST.get("firstName"),
            "email":            request.POST.get("email"),
            "phone":            request.POST.get("phone"),
            "city":             request.POST.get("city"),
            "pass1":            request.POST.get("pass1"),
            "lastName":         request.POST.get("lastName"),
            "homeAddress":      request.POST.get("homeAddress"),
            "speciality":       request.POST.get("speciality"),
            "postcode":         request.POST.get("postcode"),
            "level":            request.POST.get("level"),
            "pass2":            request.POST.get("pass2")
        }

        for i, j in information.items():
            print(f'{i} => {j}')

        if information['pass1'] != information['pass2']:
            information["border"] = "password"
            return render(request, "signup.html", information)

        filteration = freelancer.objects.all()

        if filteration.filter(email = information["email"]).exists():
            information["border"] = "email"
            return render(request, "signup.html", information)

        if filteration.filter(phone = information["phone"]).exists():
            information["border"] = "phone"
            return render(request, "signup.html", information)
 

        newFreelancer = freelancer(
            firstName   = information["firstName"],
            lastName    = information["lastName"],
            email       = information["email"],
            phone       = information["phone"],
            city        = information["city"],
            homeAddress = information["homeAddress"],
            speciality  = information["speciality"],
            postcode    = information["postcode"],
            level       = information["level"]
        )
        newFreelancer.save()

        newUser = User.objects.create_user(username=information["email"], first_name=information["firstName"], password=information["pass1"], ifFreelancer=newFreelancer)
        newUser.save()

        messages.info(request, "Your account has been created successfully!")


    return redirect("login")