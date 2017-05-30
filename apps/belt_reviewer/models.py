from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validCheck(self, form_data):
        print 'You are inside the validCheck'
        result = {"valid": True}
        errors = []
        if len(form_data['first_name'])<2 or len(form_data['last_name'])<2:
            errors.append("First and last name must be at least 2 characters long.")
            result["valid"]=False
        if not form_data['first_name'].isalpha() or not form_data['last_name'].isalpha():
            result["valid"]=False
            errors.append("Please enter a name using letters only.")
        if not EMAIL_REGEX.match(form_data['email']):
            result["valid"]=False
            errors.append("Please enter a valid email address.")
        if User.objects.filter(email = form_data['email']).first():
            result["valid"]=False
            errors.append("That email is already taken.")
        if len(form_data['password'])<8:
            result["valid"]=False
            errors.append("Password must be at least 8 characters.")
        if str(form_data['password']) != str(form_data['password_confirmation']):
            result["valid"]=False
            errors.append("Password confirmation does not match password.")
        result['errors'] = errors
        return result

    def createUser(self, form_data):
        password = form_data['password'].encode()
        #Encrypt user's password
        encryptedpw = bcrypt.hashpw(password, bcrypt.gensalt())
        user=User.objects.create(first_name=form_data['first_name'], last_name=form_data['last_name'], email=form_data['email'], password=encryptedpw)
        return user

    def logging_in(self, form_data):
        result = {"valid": True}
        errors = []
        # print form_data['email']
        user=User.objects.filter(email=form_data['email']).first()
        print user.first_name
        # print 'this is {}'.format(user)
        if user:
            print user.last_name
            password=form_data['password'].encode()
            user_pass=user.password.encode()
            if bcrypt.hashpw(password, user_pass) == user_pass:
                result['user']=user
                print 'it worked?'
                return result
        if user == None:
            errors.append("That email does not exist")
        elif bcrypt.hashpw(password, user_pass) != user_pass:
            errors.append('Invalid password')
        result["valid"] = False
        result['errors'] = errors
        return result




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirmation = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name='reviews')
    book = models.ForeignKey(Book, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
