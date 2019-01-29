from django.db import models
from django.contrib.auth.models import User #importing User model
# Create your models here.


class UserProfileInfo(models.Model): #inheritance

    user = models.OneToOneField(User, on_delete=models.PROTECT) #User is default it has already username,fname,lname,and email

    #additional
    portfolio_site = models.URLField(blank=True) #if user not fill error will not be thrown

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)#profile pic is the file name in media where the profile image will be saved

    def __str__(self):#for printitng
        return self.user.username#user name is the defalt attribute of User
