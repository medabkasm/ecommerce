# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.auth.models import (
    User ,
    AbstractBaseUser,
    BaseUserManager
    )
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from	django.utils.translation	import	gettext_lazy	as	_


class UserManager(BaseUserManager):
    #def get_by_natural_key(email):
    def create_user(self,email,username,phone ,password = None,is_active = True,is_staff = False ,is_admin = False):
        if not email:
            raise ValueError('Email required ')
        if not password:
            raise ValueError('Password required ')
        if not username:
            raise ValueError('User name required')
        if not phone:
            raise ValueError('Phone Number required')

        user_obj = self.model(
            email = self.normalize_email(email),
            username = username,
            phone = phone,
            )
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        #user_obj.active = is_active
        user_obj.save(using = self._db)

        return user_obj

    def create_staffUser(self,email,username,phone,password = None):
        user = self.create_user(
            email,
            username,
            phone,
            password = password,
            is_staff = True,
        )
    def create_superuser(self,email ,phone ,username,password = None):
        user = self.create_user(
            email,
            username,
            phone,
            password = password,
            is_staff = True,
            is_admin = True,
        )

class customUser(AbstractBaseUser):
    email = models.EmailField(max_length = 255 , unique = True)
    username = models.CharField(max_length = 40 , unique = True)
    phone = models.CharField(max_length = 20 , unique = True)
    slug = models.SlugField(max_length=150)
    #active = models.BooleanField(default = True)
    is_active =  models.BooleanField(default = True)
    staff = models.BooleanField(default = True)
    admin = models.BooleanField(default = False)
    timestamp = models.DateField(auto_now_add = True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone',]



    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username
    def get_short_name(self):
        return self.username
    @property
    def is_staff(self):
        return self.staff
    @property
    def active(self):
        return self.is_active
    @property
    def is_admin(self):
        return self.admin
    def has_module_perms(self,app_label):
        return True
    def has_perm(self,perm,obj=None):
        return True
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        return super(customUser, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:user_account',kwargs = {'slug':self.slug})


class userFollowers(models.Model):
    user = models.OneToOneField(customUser, on_delete = models.CASCADE)  # user that is been followed
    date = models.DateTimeField(auto_now_add=True)
    #count = models.IntegerField(default=1)
    followers = models.ManyToManyField(customUser,related_name='followers')
    def __str__(self):
        return '{} - {} followers '.format(self.user.username,self.count)

# Create your models here.
class Profile(models.Model):
    PROFILE_TYPE = (
        ('seler',_('Seler')),
        ('normal',_('Normal')),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE )
    profile_not_edited = models.BooleanField(default ='True')
    first_name = models.CharField(max_length = 255)
    type = models.CharField(max_length = 7 ,choices = PROFILE_TYPE,default = 'Normal')
    last_name = models.CharField(max_length = 255)
    image = models.ImageField(upload_to = 'usersImages',blank=True)
    #phone = models.CharField(max_length = 15 , blank = True)
    address = models.CharField(max_length = 255 , blank = True)
    country = models.CharField(max_length = 20)
    state = models.CharField(max_length= 20)

    @receiver(post_save, sender=customUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=customUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return '%s Profile'%(self.user.username)



class userPosts(models.Model):

    OFFER = (
        ('selling',_('Selling')),
        ('Buying',_('Buying')),
            )

    STATUS = (
			('hide',_('Hide')),
			('publish',_('Publish')),
				)

    NEGOTIATION = (
        ('accept',_('Accept')),
        ('refuse',_('Refuse')),
    )
    PHONE_STATUS = (
    ('4/10','4/10'),('5/10','5/10'),('6/10','6/10'),
    ('7/10','7/10'),('8/10','8/10'),('9/10','9/10'),
    ('10/10','10/10'),
    )
    profile = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE ,related_name = 'post' )
    name = models.CharField(max_length =255)
    offer = models.CharField(choices = OFFER , max_length = 20 ,default = 'selling')
    phone = models.CharField(max_length = 20 )
    publish	= models.DateTimeField(default=timezone.now)
    created	= models.DateTimeField(auto_now_add=True)
    updated	= models.DateTimeField(auto_now=True)
    status	= models.CharField(max_length=10,choices=STATUS,default='publish')
    exchange = models.CharField(choices = NEGOTIATION ,max_length = 20 ,default= 'refuse')
    negotiation = models.CharField(choices = NEGOTIATION ,max_length = 20 ,default= 'accept')
    price = models.DecimalField( max_digits=15,decimal_places=5)
    wilaya = models.CharField(max_length=10)
    description = models.TextField(blank = True)
    phoneStatus = models.CharField(choices = PHONE_STATUS,max_length =5,default = '10')
    coverImg = models.ImageField(upload_to = 'postimages',blank = True , null = True)

    def __str__(self):
        return '%s Post'%(self.profile.username)

    class Meta:
        ordering = ('-publish',)


    def get_absolute_url(self):
        return reverse('home:post',kwargs = {'username':self.profile.username,'id':self.id})


class Image(models.Model):
    post = models.ForeignKey(userPosts,on_delete=models.CASCADE ,related_name = 'postImage' )
    image = models.ImageField(upload_to = 'postimages',blank = True,null = True)

    def __str__(self):
        return self.post.profile.username +' images  post - %s - %s '%(str(self.post.name),str(self.post.pk))

class message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE ,related_name = 'sender' )
    receiver = models.ForeignKey(userPosts,on_delete=models.CASCADE ,related_name = 'receiver')
    created	= models.DateTimeField(auto_now_add=True)
    content = models.TextField()
