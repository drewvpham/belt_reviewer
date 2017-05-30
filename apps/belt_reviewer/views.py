from django.shortcuts import render, redirect
from models import *
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect(reverse('books'))
    return render(request, 'belt_reviewer/index.html')


def register(request):
    if request.method=='POST':
        check=User.objects.validCheck(request.POST)
        if check['valid']==True:
            user=User.objects.createUser(request.POST)
            request.session['user_id']=user.id
            return redirect(reverse('books'))
        for error in check['errors']:
            messages.error(request, error)
    return redirect(reverse('landing'))


def login(request):
    if request.method=='POST':
        logger=User.objects.logging_in(request.POST)
        print logger
        if logger['valid']==True:
            name=logger['user'].first_name
            context={'name': name}
            request.session['user_id']=logger['user'].id
            return redirect(reverse('books'))
    return redirect(reverse('landing'))

def books(request):
    if 'user_id' in request.session:
        name=User.objects.filter(id=request.session['user_id']).first().first_name
        books=Book.objects.all()
        reviews=Review.objects.all()
        context={'name': name, 'books':books, 'reviews':reviews}

        return render(request, 'belt_reviewer/books.html', context)

def add_book(request):
    if request.method=='POST' and request.session['user_id']:
        new_book=Book.objects.create(title=request.POST['title'], author=request.POST['author'])
        user=User.objects.get(id=request.session['user_id'])
        new_review=Review.objects.create(content=request.POST['review'], book=new_book, reviewer=user)
        return redirect(reverse('books'))
    authors=Book.objects.all()
    context={'authors':authors}
    return render(request, 'belt_reviewer/add_book.html', context)


def users(request, id):
    user=User.objects.filter(id=id).first()
    context={'user':user}
    return render(request, 'belt_reviewer/users.html', context)



def logout(request):
    request.session.pop('user_id')
    return redirect(reverse('landing'))
