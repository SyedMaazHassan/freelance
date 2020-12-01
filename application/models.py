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
    start_time      = models.TimeField()
    end_time        = models.TimeField()
    task_types      = models.TextField()
    group_types     = models.TextField()
    posted_date     = models.DateTimeField(default = datetime.now())
    posted_by       = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    status          = models.CharField(max_length = 50, default = "Open")

    def get_total_hours(self):
        return self.total_days * self.hours_per_day

    def when_posted(self):
        naive = self.posted_date.replace(tzinfo=None)
        myDf = datetime.now() - naive
        days, hours, minutes = myDf.days, myDf.seconds // 3600, myDf.seconds % 3600 / 60.0
        days, hours, minutes = int(days), int(hours), int(minutes)
        print(days, hours, minutes)
        print("days", "hours", "minutes")

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
                if minutes >= 1:
                    if minutes == 1:
                        return f'{minutes} minute ago'
                    return f'{minutes} minutes ago'
                else:
                    if myDf.seconds > 0 and myDf.second < 20:
                        return "Just now"

                    return f'{myDf.seconds} seconds ago'
               

    def save(self, *args, **kwargs):
        if not self.pk:
            self.end_time = self.start_time
        super(job, self).save(*args, **kwargs)
   
class client(models.Model):
    # additional fields
    fullName    = models.CharField(max_length = 25)
    city        = models.CharField(max_length = 25)
    postcode    = models.CharField(max_length = 25)
    email       = models.CharField(max_length = 25)
    homeAddress = models.CharField(max_length = 50)
    kvkNumber   = models.CharField(max_length = 25)

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