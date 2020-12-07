from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User, auth
from django.contrib.auth.models import AbstractUser
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


class job(models.Model):
    title           = models.CharField(max_length = 255)
    description     = models.TextField()
    location        = models.CharField(max_length = 255)
    total_days      = models.IntegerField()
    hours_per_day   = models.IntegerField()
    start_date      = models.DateField(default = None, blank = True, null = True)
    start_time      = models.TimeField()
    end_time        = models.TimeField()
    task_types      = models.TextField()
    group_types     = models.TextField()
    note            = models.TextField(default = None, blank = True, null = True)
    posted_date     = models.DateTimeField(default = datetime.now())
    posted_by       = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    status          = models.CharField(max_length = 50, default = "open")

    def get_total_hours(self):
        return self.total_days * self.hours_per_day

    def when_posted(self):
        postedDate = str(self.posted_date).split("+")[0]
        postedDate = datetime.strptime(postedDate, "%Y-%m-%d %H:%M:%S.%f")
        myDf = datetime.now() - postedDate
        days =  int(myDf.days)
        hours = int(myDf.seconds // 3600)
        minutes = (myDf.seconds %  3600) / 60.0


        if days > 1:
            return self.posted_date
        else:
            if days == 1:
                return f'{days} day ago'
        
            if hours >= 1:
                if hours == 1:
                    return f'{hours} hour ago'
                return f'{hours} hours ago'
            else:
                
                if myDf.seconds > 60:
                    minutes = int(minutes)                    
                    if minutes == 1:
                        return "Just now"
                    if minutes-1 == 1:
                        return f'{minutes-1} minute ago'
                    return f'{minutes-1} minutes ago'
                else:
                    if myDf.seconds <= 20:
                        return "Just now"

                    return f'{myDf.seconds} seconds ago'
               

    def save(self, *args, **kwargs):
        if not self.pk:
            self.end_time = self.start_time
        super(job, self).save(*args, **kwargs)
   
class client(models.Model):
    # additional fields
    organization_name = models.CharField(max_length = 50, default = None)
    kvkNumber   = models.CharField(max_length = 25)
    email       = models.CharField(max_length = 25)
    phone       = models.CharField(max_length = 15, default = None)
    firstName    = models.CharField(max_length = 25, default = None)
    lastName    = models.CharField(max_length = 25, default = None)
    homeAddress = models.CharField(max_length = 50)
    addressNumber = models.CharField(max_length = 50, default = None)
    postcode    = models.CharField(max_length = 25)
    city        = models.CharField(max_length = 25)


class freelancer(models.Model):
    firstName   = models.CharField(max_length = 25)
    lastName    = models.CharField(max_length = 25)
    email       = models.CharField(max_length = 25)
    phone       = models.CharField(max_length = 25)
    city        = models.CharField(max_length = 25)
    homeAddress = models.CharField(max_length = 50)
    speciality  = models.TextField()
    postcode    = models.CharField(max_length = 25)
    level       = models.CharField(max_length = 25)


class User(AbstractUser):
    ifClient = models.ForeignKey(client, on_delete = models.CASCADE, blank = True, null = True)
    ifFreelancer = models.ForeignKey(freelancer, on_delete = models.CASCADE, blank = True, null = True)

