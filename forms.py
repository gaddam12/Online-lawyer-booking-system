from django import forms
from clientapp.models import Client, Book_lawyer, Feedback, Admin, Book_Services, Add_Feedback, Add_Queries, Manage


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ["status"]


class Book_lawyerForm(forms.ModelForm):
    class Meta:
        model = Book_lawyer
        fields = ['client', 'lawyer', 'description', 'date', 'time']


class Books_lawyerForm(forms.ModelForm):
    class Meta:
        model = Book_lawyer
        fields = ["cost", "comments"]


class Manage_Forms(forms.ModelForm):
    class Meta:
        model = Manage
        fields = "__all__"


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = "__all__"


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = "__all__"


class Book_ServicesForms(forms.ModelForm):
    class Meta:
        model = Book_Services
        exclude = ["status"]


class Add_FeedbackForms(forms.ModelForm):
    class Meta:
        model = Add_Feedback
        fields = "__all__"


class Add_QueriesForms(forms.ModelForm):
    class Meta:
        model = Add_Queries
        exclude = ["reply_queries", "reply_queries_date_time"]
