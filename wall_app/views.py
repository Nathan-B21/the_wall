from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment
import bcrypt

def index(request):
    return render(request, 'index.html')



def register(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
            if key == 'reg_password':
                messages.error(request, value, extra_tags='reg_password')
            if key == 'confirm_pw':
                messages.error(request, value, extra_tags='confirm_pw')
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['reg_email'],
            password = hashed_password
            )
        request.session['user_id'] = user.id
        return redirect('/wall') # CHANGE TO WALL MAYBE
    
def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'log_email':
                messages.error(request, value, extra_tags='log_email')
            if key == 'log_password':
                messages.error(request, value, extra_tags='log_password')
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        user_list = User.objects.filter(email=request.POST['log_email'])
        if len(user_list) == 0:
            messages.error(request, 'We could not find a user with that email address', extra_tags='log_email')
            return redirect('/')
        else:
            user = user_list[0]
            if bcrypt.checkpw(request.POST['log_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/wall')
            else:
                messages.error(request, 'Your password was incorrect.',
                extra_tags='log_password')
                return redirect('/')
            
def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_messages': Message.objects.all(),
            'all_comments': Comment.objects.all()
        }
        return render(request, "wall.html", context)
    
def logout(request):
    request.session.flush()
    return redirect('/')

def postmessage(request):
    errors = Message.objects.message_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'postmessage':
                messages.error(request, value, extra_tags='postmessage')
        return redirect('/wall')
    else:
        usermessage = Message.objects.create(
            content = request.POST['postmessage'],
            posted_by = User.objects.get(id=request.session['user_id'])
        )
        return redirect("/wall")
    
    
def postcomment(request):
    errors = Comment.objects.comment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'postcomment':
                messages.error(request, value, extra_tags='postcomment')
        return redirect('/wall')
    else:
        message = Message.objects.get(id=request.POST['message_id'])
        usercomment = Comment.objects.create(
            message_parent = message,
            content = request.POST['postcomment'],
            posted_by = User.objects.get(id=request.session['user_id'])
        )
        return redirect("/wall")
    
def deletecomment(request):
    usercomment = Comment.objects.get(id=request.POST['comment_id'])
    usercomment.delete()
    return redirect("/wall")

def deletemessage(request):
    usermessage = Message.objects.get(id=request.POST['message_id'])
    usermessage.delete()
    return redirect("/wall")