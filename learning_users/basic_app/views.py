from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required#only user can loged out who is already logged in
def special(request):
    return HttpResponse("You ar logged in , Nice !! ")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False

    if request.method == "POST":
        #get info from both the form
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user=user_form.save()#grabbing the user form and save to db
            user.set_password(user.password)#hashing the password and then save it to db
            user.save()
            #extra information
            profile=profile_form.save(commit=False)#to avaiod error of overwrite or duplicate thr pics
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()

            registered=True
        else:
            print(user_form.errors,profile_form.errors)


    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()


    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                              'profile_form':profile_form,
                              'registered':registered})   #{} is context dictionary


def user_login(request):

    if request.method =='POST':#if user calls
        username=request.POST.get('username') #this key comes from the login html
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)#django built in authentication function,automatic authentication

        if user:#user is automatically authenticated
            if user.is_active:#checking active or not
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:#account is not active
                return HttpResponse("Account Not Active")

        else:#if user not authenticated
            print("Someone tried to login and failed !!")
            print("Username: {} and password: {}".format(username,password))
            return HttpResponse("invalid login details supplied !!")
    else:#not called by users
        return render(request,'basic_app/login.html',{})
