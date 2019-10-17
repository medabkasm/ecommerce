# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import Http404, HttpResponse ,HttpResponseNotFound
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import *
from .forms import *
from profiles.forms import *
from .filters import postFilter
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from	django.http	import	JsonResponse
from django.template.loader import render_to_string
from django.template import Context
import json
# Create your views here.

# search_form = searchForm() # a search form , to be available for all pages , and redirected after a post request to the main page to get search results

@login_required
class userAccountView(generic.ListView):
    template_name = 'accounts/home/customUser_list.html'
    def get_queryset(self):
        return customUser.objects.all()


@login_required
def userAccountDetailView(request,slug):
    user = request.user
    username = str(slug)
    if request.method == 'POST':
        pass

    if user.is_authenticated and user.profile.profile_not_edited :
        return redirect('profiles:edit_profile',user.username)

    else:

        print('im in get')
        try:
            object = customUser.objects.get(username = username)
            posts = userPosts.objects.filter(profile = object)
        except:
            #raise Http404()
            return HttpResponseNotFound(render(request, "accounts/404_error.html"))


        search_form = searchForm()
        return render(request,'accounts/home/customUser_detail.html',{'object':object,'posts':posts,'search':search_form,'allow_search':True})



def usersPostsView(request):

    user = request.user
    if user.is_authenticated and user.profile.profile_not_edited :
        return redirect('profiles:edit_profile',user.username)

    else:
        if request.method == 'POST':
            #filter_form = filterForm(request.POST)
            search_form = searchForm(request.POST)
            if search_form.is_valid():  # check request post from the search bar
                search = search_form.cleaned_data['search']
                model = userPosts.objects.filter(name__icontains = search , status = 'publish')
                if model.count() == 0:
                    message = _('Results Not Found ')
                else:
                    message = _('%(number)d Posts founded ')%{'number':model.count()}
            '''
            elif filter_form.is_valid():
                filter = filter_form.cleaned_data
                model = userPosts.objects.filter(name__icontains = filter['name'],
                                                status = 'publish',
                                                phoneStatus = filter['phoneStatus'],
                                                price__gte = filter['min_price'],
                                                price__lte = filter['max_price'],
                                                exchange = filter['exchange'],
                                                offer = filter['offer'],
                                                description__icontains = filter['description'],
                                                wilaya__icontains = filter['wilaya'],
                                                    )
                if model.count() == 0:
                    message = _('Results Not Found ')
                else:
                    message = _('%(number)d Posts founded ')%{'number':model.count())
            '''

			#form = postEditForm(instance = post ,data = request.POST ,files = request.FILES)
            return render(request,'accounts/home/posts.html',{'posts':model,'search': search_form,'message':message,'allow_search':True})

        search_form = searchForm()
        #filter_form = filterForm()
        #filter_form =postFilter(request.GET,queryset=Product.objects.filter(status = 'publish'))
        model = userPosts.objects.filter(status = 'publish')
        return render(request,'accounts/home/posts.html',{'posts':model,'search': search_form,'allow_search':True})




def postDetailsView(request,username,id):
        user = request.user
        if user.is_authenticated and user.profile.profile_not_edited :
            return redirect('profiles:edit_profile',user.username)
        else:
            post = userPosts.objects.get(profile__username = username , id = id )
            search_form = searchForm()
            if post :
                found = 'post found'
            else:
                found = 'post not found'
            return render(request,'accounts/home/userPosts_detail.html',{'post':post ,'search': search_form,'allow_search':True,'found':found})



def	register(request):
    search_form = searchForm()
    if	request.method	==	'POST':
        form = UserCreationForm(request.POST)
        #profileForm = profileEditForm(request.POST,request.FILES)

        if	form.is_valid() :
            #	Create	a	new	user	object	but	avoid	saving	it	yet
            new_user = form.save(commit=False)
            #	Set	the	chosen	password
            new_user.set_password(form.cleaned_data['password1'])
            #new_profile = profileForm.save()
            #new_user.profile = new_profile
            #	Save	the	User	object
            new_user.save()
            return	render(request,'accounts/register_done.html',{'new_user': new_user,'search': search_form})

    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home:users_posts')
        form = UserCreationForm()
           #profileForm = profileEditForm()
    return	render(request,'accounts/register.html',{'form':form,'search': search_form})

@require_POST
@login_required
def userFollow(request):

    if request.method == "POST": #os request.GET()
        #username = request.POST.get('username')
        print('hello')
        # Do your logic here coz you got data in `get_value`
        data = {}
        data['result'] = 'you made a request'
        return HttpResponse(json.dumps(data), content_type="application/json")





@require_POST
@login_required
def sendEmail(request,slug):
    username = str(slug)
    user = customUser.objects.get(username = username)
    email = user.email

    if request.method == 'POST':
        form = emailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_mail = (str(data['subject']),str(data['my_message']),str(data['your_email']),[str(email),'mohamed_akasm@outlook.com',])
            message_sent = True
    else:
        form = emailForm()
        message_sent = False
    return render(request,'home:')
