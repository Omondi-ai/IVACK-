from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Thread, Message
from .forms import MessageForm, NewThreadForm
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

@login_required
def inbox(request):
    threads = Thread.objects.filter(participants=request.user).order_by('-updated')
    return render(request, 'messaging/inbox.html', {'threads': threads})

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender = request.user
            message.save()
            
            # Mark other user's messages as read
            Message.objects.filter(thread=thread).exclude(sender=request.user).update(is_read=True)
            
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = MessageForm()
    
    messages = thread.message_set.all().order_by('created')
    other_user = thread.participants.exclude(id=request.user.id).first()
    
    return render(request, 'messaging/chat.html', {
        'thread': thread,
        'messages': messages,
        'other_user': other_user,
        'form': form,
    })

@login_required
def new_thread(request):
    if request.method == 'POST':
        form = NewThreadForm(request.POST, user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            message_text = form.cleaned_data['message']
            
            # Check if thread already exists
            thread = Thread.objects.filter(participants=request.user).filter(participants=recipient).first()
            
            if not thread:
                thread = Thread.objects.create()
                thread.participants.add(request.user, recipient)
            
            # Create the message
            Message.objects.create(
                thread=thread,
                sender=request.user,
                text=message_text
            )
            
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = NewThreadForm(user=request.user)
    
    return render(request, 'messaging/new_message.html', {'form': form})