from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from clientapp.models import Client, Book_lawyer, Feedback, Book_Services, Add_Feedback, Add_Queries, Manage
from clientapp.forms import ClientForm, Book_lawyerForm, FeedbackForm, Book_ServicesForms, Add_FeedbackForms, \
    Add_QueriesForms, Manage_Forms
from lawyerapp.models import Lawyer, Services
from lawapp.models import Notifications


# Create your views here.


def client_is_login(request):
    if request.session.__contains__("email"):
        return True
    else:
        return False


def client_home(request):
    return render(request, "client_home.html", {})


def client_details(request):
    email = request.session["email"]
    client = Client.objects.get(email=email)
    print(email)
    return render(request, "client_details.html", {"client": client})


def client_change_password(request):
    email = request.session['email']
    if client_is_login(request):
        if request.method == "POST":
            password = request.POST["old_password"]
            new_password = request.POST["new_password"]
            if password == new_password:
                return render(request, "client_change_password.html",
                              {"msg": "Your Old And New Passwords Are Same", "email": email})
            try:
                users = Client.objects.get(email=email, password=password)
                users.password = new_password
                users.save()
                messages.success(request, "Successfully Password Updated")
                return redirect('/client_login')
            except Exception as e:
                print(e)
                return render(request, 'client_change_password.html', {"msg": "Invalid Creditinals", "email": email})
        return render(request, 'client_change_password.html', {"email": email})
    else:
        return redirect('/client_login')


def client_edit(request, email):
    client = Client.objects.get(email=email)
    return render(request, "client_update.html", {"client": client})


def client_update(request):
    if request.method == 'POST':
        email = request.POST["email"]
        client = Client.objects.get(email=email)
        form = ClientForm(request.POST, request.FILES, instance=client)
        print(form.errors)
        if form.is_valid():
            form.save()
        return redirect('/client_details')
    return render(request, 'client_update.html', {})


def client_delete(request, email):
    client = Client.objects.get(email=email)
    client.delete()
    return redirect("/client_registration")


def client_lawyers(request):
    lawyers = Lawyer.objects.all()
    return render(request, "client_lawyers.html", {"lawyers": lawyers})


# def book_lawyer(request, pk):
#     email = request.session["email"]
#     client = Client.objects.get(email=email)
#     lawyer = Lawyer.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = Book_lawyerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/booked")
#     return render(request, "book_Lawyers.html", {"client": client.email, "lawyer": lawyer.email})


from django.core.mail import send_mail
from .models import Client, Lawyer, Book_lawyer
from .forms import Book_lawyerForm
from django.shortcuts import render, redirect

from django.contrib import messages


def book_lawyer(request, pk):
    email = request.session["email"]
    client = Client.objects.get(email=email)
    lawyer = Lawyer.objects.get(pk=pk)

    if request.method == 'POST':
        form = Book_lawyerForm(request.POST, request.FILES)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            # 🔍 Check if the same lawyer is already booked at the same date and time
            if Book_lawyer.objects.filter(lawyer=lawyer, date=date, time=time).exists():
                messages.error(request, "This time slot is already booked. Please choose another time.")
                return render(request, "book_Lawyers.html", {
                    "form": form,
                    "client": client.email,
                    "lawyer": lawyer.email
                })

            # ✅ Save the booking
            booking = form.save(commit=False)
            booking.client = client
            booking.lawyer = lawyer
            booking.save()

            # ✉️ Send confirmation to client
            client_subject = "Booking Confirmation - Online Lawyer Booking"
            client_message = f"""Dear {client.full_name},

Thanks for booking with us. Your appointment request has been sent to {lawyer.full_name}.
You will be contacted soon.

Regards,
Online Lawyer Booking Team"""

            # ✉️ Notify the lawyer
            lawyer_subject = "New Booking Received"
            lawyer_message = f"""Dear {lawyer.full_name},

You have received a new booking from {client.full_name}.

Please login to your account to check the details.

Regards,
Online Lawyer Booking Team"""

            try:
                send_mail(client_subject, client_message, 'devteamhub25@gmail.com', [client.email], fail_silently=False)
                send_mail(lawyer_subject, lawyer_message, 'devteamhub25@gmail.com', [lawyer.email], fail_silently=False)
            except Exception as e:
                print("Email sending failed:", e)

            return redirect("/booked")
    else:
        form = Book_lawyerForm()

    return render(request, "book_Lawyers.html", {
        "form": form,
        "client": client.email,
        "lawyer": lawyer.email
    })


#
# def book_lawyer(request, pk):
#     email = request.session["email"]
#     client = Client.objects.get(email=email)
#     lawyer = Lawyer.objects.get(pk=pk)
#
#     if request.method == 'POST':
#         form = Book_lawyerForm(request.POST, request.FILES)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.client = client
#             booking.lawyer = lawyer
#             booking.save()
#
#             # ✅ Send confirmation to client
#             client_subject = "Booking Confirmation - Online Lawyer Booking"
#             client_message = f"""Dear {client.full_name},
#
# Thanks for booking with us. Your appointment request has been sent to {lawyer.full_name}.
# You will be contacted soon.
#
# Regards,
# Online Lawyer Booking Team"""
#
#             # ✅ Send notification to lawyer
#             lawyer_subject = "New Booking Received"
#             lawyer_message = f"""Dear {lawyer.full_name},
#
# You have received a new booking from {client.full_name}.
#
# Please login to your account to check the details.
#
# Regards,
# Online Lawyer Booking Team"""
#
#             try:
#                 send_mail(client_subject, client_message, 'devteamhub25@gmail.com', [client.email], fail_silently=False)
#                 send_mail(lawyer_subject, lawyer_message, 'devteamhub25@gmail.com', [lawyer.email], fail_silently=False)
#             except Exception as e:
#                 print("Email sending failed:", e)
#
#             return redirect("/booked")
#     else:
#         form = Book_lawyerForm()
#
#     return render(request, "book_Lawyers.html", {
#         "form": form,
#         "client": client.email,
#         "lawyer": lawyer.email
#     })


def clients_view_feedbacks(request, pk):
    lawyers = Lawyer.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(lawyer=lawyers.email)
    return render(request, "clients_view_feedbacks.html", {"feedbacks": feedbacks})


def booked(request):
    email = request.session["email"]
    client = Client.objects.get(email=email)
    form = Book_lawyer.objects.filter(client_id=client.email)
    return render(request, "booked.html", {"forms": form, "client": client})


def feedback(request, id):
    email = request.session['email']
    client = Client.objects.get(email=email)
    forms = Book_lawyer.objects.get(id=id)
    if request.method == "POST":
        booked = FeedbackForm(request.POST)
        print(booked.errors)
        if booked.is_valid():
            booked.save()
            lawyer = get_object_or_404(Lawyer, email=forms.lawyer_id)  # Assuming `lawyer_id` stores the email
            return redirect(f"/clients_view_feedbacks/{lawyer.pk}")
    return render(request, "feedback.html",
                  {"client": forms.client_id, 'customer': client, "forms": forms, "email": email})


def client_logout(request):
    if request.session.has_key('email'):
        del request.session['email']
    return render(request, "client_login.html.", {"msg": ""})


def client_view_notification(request):
    cnote = Notifications.objects.all()
    return render(request, 'client_view_notification.html', {"cnote": cnote})


def client_view_services(request, pk):
    lawyer = Lawyer.objects.get(pk=pk)
    services = Services.objects.filter(email=lawyer.email)
    return render(request, "client_view_services.html", {"services": services})


def book_services(request, id):
    email = request.session["email"]
    services = Services.objects.get(id=id)
    if request.method == 'POST':
        form = Book_ServicesForms(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

            return redirect("/clients_view_bookings_services")
    return render(request, "book_services.html", {"services": services, "email": email})


def clients_view_bookings_services(request):
    email = request.session["email"]
    bookings = Book_Services.objects.filter(email=email)
    return render(request, "clients_view_bookings_services.html", {"bookings": bookings})


# def add_feedback(request, id):
#     email = request.session['email']
#     bookings = Book_Services.objects.get(id=id)
#     if request.method == "POST":
#         booked = Add_FeedbackForms(request.POST)
#         print(booked.errors)
#         if booked.is_valid():
#             booked.save()
#
#             return redirect(f"/clients_services_view_feedbacks/{id}")
#     return render(request, "add_feedback.html", {"bookings": bookings, "email": email})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book_Services
from .forms import Add_FeedbackForms

def add_feedback(request, id):
    email = request.session.get('email')
    try:
        bookings = Book_Services.objects.get(id=id)
    except Book_Services.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect("some_error_page")  # Optional

    if request.method == "POST":
        booked = Add_FeedbackForms(request.POST)
        print(booked.errors)

        if booked.is_valid():
            booked.save()
            service_id = bookings.services.id
            # messages.success(request, "Thanks for adding your feedback!")
            return redirect(f"/clients_services_view_feedbacks/{service_id}")

    return render(request, "add_feedback.html", {"bookings": bookings, "email": email})



def clients_services_view_feedbacks(request, id):
    services = Services.objects.get(id=id)
    feedbacks = Add_Feedback.objects.filter(services_id=services.id)
    return render(request, "clients_services_view_feedbacks.html", {"feedbacks": feedbacks})


def add_queries(request, pk):
    email = request.session['email']
    lawyers = Lawyer.objects.get(pk=pk)
    if request.method == "POST":
        queries = Add_QueriesForms(request.POST)
        print(queries.errors)
        if queries.is_valid():
            queries.save()
            return redirect("/my_quries")
    return render(request, "add_queries.html", {"lawyers": lawyers, "email": email})


def my_quries(request):
    email = request.session['email']
    quries = Add_Queries.objects.filter(email=email)
    return render(request, "my_quries.html", {"quries": quries})


def manage_clients(request, id):
    email = request.session["email"]
    lawyer = Book_lawyer.objects.get(id=id)
    if request.method == 'POST':
        form = Manage_Forms(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect(f"/manage_files_clients/{id}")
    return render(request, "manage_clients.html", {"forms": lawyer, "email": email})


def manage_files_clients(request, id):
    email = request.session.get("email")
    lawyer = Book_lawyer.objects.get(id=id)
    files = Manage.objects.filter(lawyer_id=lawyer.id)
    return render(request, "manage_files_clients.html", {"files": files, "email": email})


def delete_files_clients(request, id):
    file = get_object_or_404(Manage, id=id)
    lawyer_id = file.lawyer_id
    file.delete()
    return redirect(reverse("manage_files_clients", args=[lawyer_id]))
