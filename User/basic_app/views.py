from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm 

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special_page(request):
    return HttpResponse('NICE YOU LOG IN')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered=False

    if request.method=="POST":
        form=UserForm(request.POST)
        p_form=UserProfileInfoForm(request.POST)
        if (form.is_valid() and p_form.is_valid()):
            USER=form.save()
            USER.set_password(USER.password)
            USER.save()
                
            profile=p_form.save(commit=False)
            profile.USER=USER

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
            print(form.errors,p_form.errors)
        
    else:
        form=UserForm()
        p_form=UserProfileInfoForm()
    return render(request,'basic_app/registration.html',{'form':form,'p_form':p_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('user_name')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        t = authenticate(username=username, password=password)

        # If we have a user
        if t:
            #Check it the account is active
            if t.is_active:
                # Log the user in.
                login(request,t)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return render(request, 'basic_app/login.html', {})

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})
    