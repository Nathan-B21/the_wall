from django.db import models
import re

class User_Manager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['reg_email']):        
            errors['reg_email'] = "Invalid email address."
        if len(postData['reg_password']) < 8:
            errors["reg_password"] = "Please enter a password and at least 8 characters"
        if postData['reg_password'] != postData['confirm_pw']:
            errors["confirm_pw"] = "Passwords must match."
        return errors
        
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not EMAIL_REGEX.match(postData['log_email']):        
            errors['log_email'] = "Please enter a valid email address."
        if len(postData['log_password']) == 0:
            errors["log_password"] = "Please enter password"
        return errors

class Message_Manager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        if len(postData['postmessage']) < 1:
            errors['postmessage'] = "You most post a message greater than one character."
        return errors
        
    
class Comment_Manager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['postcomment']) < 1:
            errors['postcomment'] = "Your comment must be greater than one character."
        return errors








class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()
    
class Message(models.Model):
    content = models.TextField(max_length=100)
    posted_by = models.ForeignKey(User, related_name = "messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Message_Manager()

class Comment(models.Model):
    content = models.TextField(max_length=100)
    message_parent = models.ForeignKey(Message, related_name = "comments", on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, related_name = "comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Comment_Manager()
    