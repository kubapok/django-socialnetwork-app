from django.shortcuts import render,render_to_response,  get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from .models import *




def welcome(request):
    return render(request, 'socialnetwork/welcome.html', {'username': request.user.username})


def loggedin(request):
    return render(request,'registration/loggedin.html',{'username': request.user.username,})


def administration(request):
    unanswered_requests_quantity = len(FriendshipRequest.unanswered_requests_of(request.user))
    return render(request,'socialnetwork/administration.html',{'username': request.user.username, 'user':request.user, 'unanswered_requests_quantity':unanswered_requests_quantity})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register/complete')
    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render_to_response('socialnetwork/registration_form.html', token)


def registration_complete(request):
    return render_to_response('socialnetwork/registration_complete.html')


@login_required
def finduser(request):
    if request.method == "POST":
        form = FriendshipRequestForm(request.POST)
        if form.is_valid():
            friendshiprequest = form.save(commit=False)
            if Friendship.are_friends(request.user,friendshiprequest.requested):
                response = "You are already friends"
            elif FriendshipRequest.is_already_asked_by(request.user,friendshiprequest.requested):
                response = "You have already sent a request, please wait for your response"
            elif FriendshipRequest.is_already_asked_by(friendshiprequest.requested,request.user):
                response = "The request from this user was sent to you before, please respond to your request"
            elif request.user == friendshiprequest.requested:
                response = "You can not sent a friendship request to yourself"
            else:
                friendshiprequest.creator = request.user
                friendshiprequest.answer = None
                friendshiprequest.save()
                response = 'the request to ' +  str(friendshiprequest.requested) + ' has been sent'
            return render(request, 'socialnetwork/finduser.html', {'form': form, 'response' : response, 'username': request.user.username})
    else:
        form = FriendshipRequestForm()
    return render(request, 'socialnetwork/finduser.html', {'form': form,'username': request.user.username})



@login_required
def friendshiprequestslist(request):
    no_requests_info = False if FriendshipRequest.is_any_unanswered(request.user) else True
    if request.method == "POST":
        pk = int(request.POST['pk']) #primary key depending on which button was submitted
        answer = {'1':None, '2':True, '3':False}[request.POST['answer']] #answer to question
        r = FriendshipRequest.objects.get(pk=pk)
        r.answer = answer
        response = str(answer) + str(pk) + str(r.creator)
        r.save()
        if answer==True:
            Friendship.create_friendship(r.creator, r.requested)
    else:
        response = None
    requestslist = FriendshipRequest.unanswered_requests_of(request.user)
    form = RespondToRequestsForm(initial={'answer': None})
    return render(request, 'socialnetwork/friendshiprequests.html', {'requestslist': requestslist, 'form': form, 'response':response,'username': request.user.username, 'no_requests_info' : no_requests_info},)




@login_required
def myfriends(request):
    friendslist = Friendship.friends_of(request.user)
    no_friends = False if len(friendslist) else True
    return render(request,'socialnetwork/myfriends.html',{'username': request.user.username, 'friendslist' : friendslist, 'no_friends':no_friends })




@user_passes_test(lambda user: user.is_superuser)
def connections(request):
    if request.method == "POST":
        form = connectionsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user']
            friendslist = Friendship.friends_of(User.objects.get(username=username))
            requested_user = username.username
            if friendslist:
                response1 = "This is a list of "
                response2 = " friends:"
            else:
                response1 = "User"
                response2 = " has no friends"
            return render(request, 'socialnetwork/connections.html', {'form': form, 'friendslist' : friendslist, 'response1' : response1, 'response2' :response2, 'requested_user':requested_user})
    else:
        form = connectionsForm()
    return render(request, 'socialnetwork/connections.html', {'form': form,'username': request.user.username})
