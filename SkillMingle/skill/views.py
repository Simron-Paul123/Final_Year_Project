from django.shortcuts import render,HttpResponse,redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Category, CustomUser, Job

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'job_seeker.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.usertype == 'recruiter' and not user.is_approved:
                return HttpResponse("Your account is awaiting admin approval.")
            
            login(request, user)
            
            if user.usertype == 'recruiter':
                return redirect('company')  # Update this with your recruiter dashboard URL
            
            elif user.usertype == 'job_seeker':
                # Check if CV is provided
                if user.cv:
                    return redirect('job_seeker')  # Update this with your job seeker dashboard URL
                else:
                    return redirect('user_dashboard')  # Redirect to a page prompting them to upload CV
            
        else:
            return HttpResponse("Username or Password is incorrect!")
    
    return render(request, 'user_reg.html')

def register_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        usertype = request.POST.get('usertype')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        if CustomUser.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists!")
        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")
        if usertype not in ['recruiter', 'job_seeker']:
            return HttpResponse("Invalid user type!")

        # Create the user
        is_approved = usertype == 'job_seeker'  # Job seekers are auto-approved
        my_user = CustomUser.objects.create_user(username=uname, email=email, password=pass1, usertype=usertype, is_approved=is_approved)
        my_user.save()
        return redirect('login')
    return render(request, 'user_reg.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def job_seeker(request):
    jobs = Job.objects.all()  # Fetch all job entries from the Job model
    categories = Category.objects.all()  # Fetch all category entries from the Category model
    return render(request, 'job_seeker.html', {'jobs': jobs, 'categories': categories})
@login_required(login_url='login')
def company(request):
    return render(request, 'company.html')
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

