from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login,logout
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .forms import ChatMessageForm
from .models import GroupMember, Group, ChatMessage, ChatReply
from django.db.models import Count


# Create your views here.

def signupview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        try:
            User.objects.create_user(username_data, '',password_data)
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'このユーザーは既に登録されています。'})
    else:
        return render(request, 'signup.html', {})
    return render(request, 'signup.html', {})

def topview(request):
    object_list = GroupMember.objects.filter(group__secret=Group.PUBLIC).annotate(Count('user')).order_by('-user__count')
    return render(request,'top.html', {'object_list':object_list})

def homeview(request):
    return render(request,'home.html')

def loginview(request):
    if request.method == 'POST':
        username_data = request.POST['username_data']
        password_data = request.POST['password_data']
        user = authenticate(request, username=username_data, password=password_data)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')

def groupview(request, pk):
    group = Group.objects.get(pk=pk)
    form = ChatMessageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.user = request.user
            chat_message.group = group
            chat_message.save()
    chat_message_list = ChatMessage.objects.filter(group = group).order_by('-created_at')
    return render(request,'group.html',{'object':group, 'chat_message_list':chat_message_list})

def chat_reply_view(request):
    group_id = request.POST['group_id']
    chat_id = request.POST['chat_id']
    reply = request.POST['reply']
    ChatReply.objects.create(
        chat_id=chat_id,
        user=request.user,
        reply=reply,
    )
    return redirect('group', group_id)

def chatview(request, group_id, chat_id):
    group_id = request.POST['group_id']
    chat_id = request.POST['chat_id']
    reply = request.POST['reply']
    ChatReply.objects.create(
        chat_id=chat_id,
        user=request.user,
        reply=reply,
    )
    return redirect(request,'chat.html')

"""
@login_required
def listview(request):
    object_list = ReviewModel.objects.all()
    return render(request, 'list.html',{ 'object_list':object_list})

@login_required
def detailview(request, pk):
    object= ReviewModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object':object})

class CreateClass(CreateView):
    template_name = 'create.html'
    model = ReviewModel
    fields = ('title', 'content', 'author', 'images', 'evaluation')
    success_url = reverse_lazy('list')

def logoutview(request):
    logout(request)
    return redirect('login')

def evaluationview(request, pk):
    post = ReviewModel.objects.get(pk=pk)
    author_name = request.user.get_username() + str(request.user.id)
    post.useful_review = post.useful_review + 1
    post.useful_review_record = post.useful_review_record + author_name
    post.save()
    return redirect('list')
"""