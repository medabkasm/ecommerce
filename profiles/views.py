from django.shortcuts import render
from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import Http404, HttpResponse ,HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views import generic
from accounts.models import *
from .forms import *
from django.forms import modelformset_factory
from accounts.forms import *

# search_form = searchForm() # a search form , to be available for all pages , and redirected after a post request to the main page to get search results


@login_required
def sharePostView(request,username):
	user = request.user
	if user.is_authenticated and user.profile.profile_not_edited :
		return redirect('profiles:edit_profile',user.username)
	else:
		search_form = searchForm()
		user = request.user
		imagesFormSet = modelformset_factory(Image,fields=('image',),extra = 5)
		if request.method == 'POST' :
			form = postForm(request.POST, request.FILES )
			formset = imagesFormSet(request.POST , request.FILES )
			#images = imageForm(request.POST,request.FILES)
			if form.is_valid() and formset.is_valid():

				data =form.cleaned_data
				new_post = userPosts.objects.create(profile = user ,name = data['name'],
								offer = data['offer'], phone = data['phone'], status = data['status'],
								wilaya = data['wilaya'], exchange = data['exchange'], negotiation = data['negotiation'],
								price = data['price'], description = data['description'], phoneStatus = data['phoneStatus'],
								coverImg = data['coverImg'],
											)
				for f in formset:
					try:
						image_for_post =Image(post = new_post ,image =  f.cleaned_data['image'])
						image_for_post.save()
					except:
						break

				return redirect('home:users_posts')

		else:
			form = postForm()
			#images = imageForm()
			formset = imagesFormSet(queryset = Image.objects.none())
		return render(request,'profiles/share_post.html',{'form':form ,'formset':formset,'search':search_form,'allow_search':True})






@login_required
def editPost(request,username,id):
	user = request.user
	if user.is_authenticated and user.profile.profile_not_edited :
		return redirect('profiles:edit_profile',user.username)
	else:
		search_form = searchForm()
		try: # check if the url is real
			post = userPosts.objects.get(pk = id)
			images = Image.objects.get(post = post)
		except:
			return redirect('users_posts',kwargs = {'allow_search':True})

			# handle the request
		if request.method == 'POST':
			form = postEditForm(instance = post ,data = request.POST ,files = request.FILES)
			image = imageEditForm(instance = images,data = request.POST ,files = request.FILES)
			if form.is_valid() and image.is_valid():
				form.save()
				image.save()
				edit_done = True
			else:
				return render(request,'profiles/editPost.html',{'form':form,'image':image,'search':search_form,'allow_search':True})
		else:
			edit_done = False
			form = postEditForm(instance = post)
			image = imageEditForm(instance = images)
		return render(request,'profiles/editPost.html',{'form':form,'images':image,'edit':edit_done,'search':search_form,'allow_search':True})




@login_required
def deletePost(request,username,id):
	user = request.user
	if user.is_authenticated and user.profile.profile_not_edited :
		return redirect('profiles:edit_profile',user.username)
	else:
		search_form = searchForm()
		post = userPosts.objects.get(pk = id )
		try:
			post.delete()
			delete = True
		except:
			delete = False
		return render(request,'profiles/deletePost.html',{'delete':delete,'search':search_form,'allow_search':True})







@login_required
def edit_profile(request,username):
	user = request.user
	if request.method == 'POST':
		profileForm = profileEditForm(instance=user.profile,
										data=request.POST,
										files=request.FILES	)

		userForm = userEditForm(instance=user,data = request.POST)
		if profileForm.is_valid() and userForm.is_valid():
			userForm.save()
			profileForm.save()
			edit_done = True
			user.profile.profile_not_edited = False # to let the user access the other pages after editing
			user.save()
		else:
			return render(request,'profiles/editProfile.html',{'profileForm':profileForm,'userForm':userForm})
	else:
		edit_done = False
		profileForm = profileEditForm(instance=user.profile)
		userForm = userEditForm(instance=user)
	return render(request,'profiles/editProfile.html',{'profileForm':profileForm,'userForm':userForm,'edit':edit_done})
