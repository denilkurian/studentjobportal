from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import ListView, CreateView,UpdateView,DetailView,DeleteView

from .forms import ReviewForm, SignupForm
from .models import profile, Jobs, Notifications, Review, Save, Company
from django.db import models

from .utils import generate_otp, send_otp_email


def welcome(request):
    return render(request,'welcome.html')
def homepage(request):
    return render(request,'homepage.html')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Generate a unique username based on the email
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                return HttpResponse('Email already exists')

            username = email.split('@')[0]
            # Generate an OTP and send it to the user's email
            otp = generate_otp()
            send_otp_email(email, otp)

            # Store the user details in the session
            request.session['username'] = username
            request.session['email'] = email
            request.session['password'] = form.cleaned_data.get('password')
            request.session['otp'] = otp

            # Redirect to the OTP verification page
            return redirect('verify_otp')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        stored_otp = request.session.get('otp')
        if otp == stored_otp:
            # Create a new user account
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Log in the user and redirect to the home page
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Invalid OTP')
    else:
        email = request.session.get('email')
        if not email:
            return redirect('signup')

    return render(request, 'otp_verification.html', {'email': email})





def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                form.add_error(None, 'Invalid login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request, 'Logout successfully.')
    return redirect('homepage')


################
##################
class TaskList(ListView):
    model= profile
    fields="__all__"
    context_object_name = 'profile'
    template_name='profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = context['profile'].filter(user=self.request.user)
        return context



class TaskCreate(CreateView):
    model = profile
    fields = ['name','email','phone','address','qualification','college','cgpa','experience','skills','complete','resume']
    success_url = reverse_lazy('profile')
    template_name = 'profile-create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)




##########
################## section under student / profile
class TaskUpdate(UpdateView):
    model = profile
    fields = ['name', 'email', 'phone', 'address', 'qualification', 'college','cgpa','experience', 'skills', 'resume', 'profile','complete']
    success_url=reverse_lazy('profile')
    template_name='profile-create.html'


class TaskDelete(SuccessMessageMixin ,DeleteView):
    model = profile
    context_object_name = 'profile-delete'
    success_message = "Deleted successfully"
    success_url = reverse_lazy('profile')
    template_name = 'profile-delete.html'



#######################
########################
class Findjob(ListView):
    model = Jobs
    fields=['role','company','location','salary','duration']
    context_object_name = 'findjob'
    template_name = 'findjob.html'




class Jobdetail(DetailView):
    model=Jobs
    fields= ['role', 'company', 'location', 'salary', 'duration', 'job_description', 'call']
    template_name ='jobdetail.html'
    context_object_name = 'every'



######### search ###########
###################
class SearchResultView(ListView):
    model = Jobs
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Jobs.objects.filter(Q(role=query)| Q(company=query))




class Filter(ListView):
    model = Jobs
    template_name = 'filter.html'

    def get_queryset(self):
        query = self.request.GET.get('f')
        return Jobs.objects.filter(Q(job_type=query))

##################-applied-jobs-###
#######################
class update(SuccessMessageMixin,UpdateView):
    model = Jobs
    fields = ['complete']
    template_name = 'update.html'
    success_message = 'Application has been submitted successfully'
    success_url = reverse_lazy('applied')







# class Applied(ListView):
#     model = Jobs
#     template_name = 'cart.html'
#     context_object_name = 'apply'






######################
#####################  Section under employer
class employer_list(ListView):
    model = Jobs
    template_name = 'employer.html'
    context_object_name = 'list'
    fields = ['job_type', 'role', 'company', 'location', 'salary', 'duration', 'job_description', 'call', 'Hired']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = context['list'].filter(user=self.request.user)
        return context


class create(SuccessMessageMixin,CreateView):
    model = Jobs
    template_name = 'employer-create.html'
    success_url = reverse_lazy('list')
    fields = ['job_type','role','company','location','salary','duration','job_description','call','Hired']
    success_message = 'Job form successfully posted'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(create, self).form_valid(form)



class updatee(SuccessMessageMixin,UpdateView):
    model = Jobs
    template_name = 'employer-create.html'
    success_url = reverse_lazy('list')
    fields = ['job_type', 'role', 'company', 'location', 'salary', 'duration', 'job_description', 'call', 'Hired']
    success_message = 'Job form successfully edited and posted'
class deletee(SuccessMessageMixin,DeleteView):
    model = Jobs
    template_name = 'employer-delete.html'
    fields = "__all__"
    success_url = reverse_lazy('list')
    success_message = 'Successfully removed from public'

class detailss(SuccessMessageMixin,DetailView):
    model = Jobs
    template_name = 'employer-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(product=self.object)
        return context


############
################ Notifications
class notlist(ListView):
    model = Notifications
    template_name = 'notifications.html'
    fields='__all__'
    context_object_name = 'notification'

class notdetail(DetailView):
    model = Notifications
    template_name = 'notification-detail'
    fields='__all__'

class notdelete(DeleteView):
    model = Notifications
    fields='__all__'
    template_name = 'notifications.html'
    success_url = reverse_lazy('notlist')



def settings(request):
    return render(request,'settings.html')



################
########################

############ application
def add_review(request, pk):
    product = get_object_or_404(Jobs, pk=pk)
    messages.success(request, 'Applied Successfully.')
    if request.method == 'POST':
        form = ReviewForm(request.POST,request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('jobdetail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'application.html', {'form': form, 'product': product})


########### applied jobs list user filtered
def my_reviews(request):
    user_reviews = Review.objects.filter(user=request.user)
    context = {'user_reviews': user_reviews}
    return render(request, 'cart.html', context)



########### delete application
def delete_review(request, review_id):
    messages.success(request, 'Application removed successfully.')
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:
        review.delete()
    return redirect('my_reviews')




########## to download the filefied
def my_detail(request, pk):
    instance = get_object_or_404(Review, pk=pk)
    file_url = instance.file.url
    return render(request, 'employer-detail.html', {'instance': instance, 'file_url': file_url})



############ count APPLication

def cart_count(request):
    if request.user.is_authenticated:
        count = Review.objects.filter(user=request.user).count()
        return JsonResponse({'count': count})
    else:
        return JsonResponse({'count': 0})

def my_view(request):
    return render(request, 'homepage.html')


########## save jobs
def add_to_save(request, saved_id):
    Product = get_object_or_404(Jobs, pk=saved_id)
    saved,created = Save.objects.get_or_create(
        user=request.user,
        job = Product

    )
    if not created:
        saved.quantity = 1
        saved.save()
    return redirect('save')


def remove_from_save(request, save_id):
    saved = get_object_or_404(Save, pk=save_id, user=request.user)
    saved.delete()
    return redirect('save')

def save(request):
    savedd = Save.objects.filter(user=request.user)
    return render(request, 'saved.html', {'saved': savedd})




################ delete user account
@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # Password is correct, delete the account
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return JsonResponse({})
        else:
            # Password is incorrect, return an error message
            return JsonResponse({'incorrect_password': True})
    else:
        return render(request, 'delete_account.html')

################ about careerbuddy

def about(request):
    return render(request,'about.html')


############# company search

class SearchCompanyView(ListView):
    model = Jobs
    template_name = 'company.html'
    context_object_name = "company"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Company.objects.filter(Q(name=query))



########## for the suggessions of js
def get_suggestions(request):
    term = request.GET.get("term", "")
    model_name = request.GET.get("model_name", "")
    field_name = request.GET.get("field_name", "")
    suggestions = Company.objects.filter(
        **{f"{field_name}__icontains": term}
    ).values_list(field_name, flat=True)[:10]
    return JsonResponse(list(suggestions), safe=False)





