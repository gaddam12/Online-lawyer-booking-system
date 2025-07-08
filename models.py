from django.db import models
from django.utils.timezone import now

from lawyerapp.models import Lawyer, Services


# Create your models here.


class Client(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    city = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    cimage = models.ImageField(upload_to='images/',null=True)
    status = models.CharField(max_length=100,default="on hold")


    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "client"


class Book_lawyer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to='images/',null=True)
    status = models.IntegerField(default=0)
    cost = models.BigIntegerField(null=True)
    comments = models.TextField(null=True)

    class Meta:
        db_table = "Book_lawyer"


class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, default=0)
    description = models.TextField()
    rating = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "client_feedback"


class Admin(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=100)


class Book_Services(models.Model):
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    email = models.EmailField()
    title = models.CharField(max_length=100)

    description = models.TextField()
    cost = models.BigIntegerField()
    date_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100,default="Pending")

    class Meta:
        db_table = "Book_Services"



class Add_Feedback(models.Model):
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    email = models.EmailField()
    description = models.TextField()
    rating = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now=True)
    class Meta:

        db_table = "Add_Feedback"

class Add_Queries(models.Model):
    lawyers = models.ForeignKey(Lawyer, on_delete=models.CASCADE, default=0)
    email = models.EmailField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField(auto_now=True)

    reply_queries = models.TextField(default="None")
    reply_queries_date_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "Add_Queries"

    def save(self, *args, **kwargs):
        # Automatically set reply_queries_date_time when reply_queries is updated
        if self.reply_queries and self.reply_queries != "None":
            self.reply_queries_date_time = now()
        super().save(*args, **kwargs)

class Manage(models.Model):
    lawyer = models.ForeignKey(Book_lawyer, on_delete=models.CASCADE)
    upload_by = models.EmailField()
    file = models.FileField()
    date_time = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "Manage"
