from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from ..login.models import *
from . models import Wish

def current_user(request):
    return User.objects.get(id=request.session['user_id'])

def flash_errors(request, errors):
    for error in errors:
        messages.error(request, error)

def user(request, id):
    context={
        'user' : current_user(request),
    }
    return render(request, 'item.html', context)

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = current_user(request)
    context = {
        'user': user, 
        'notwished': Wish.objects.exclude(wished_by = user),
    }
    return render(request, 'wish/index.html', context)

def show_wish(request, wish_id):
    wish = Wish.objects.get(id = wish_id)
    context = {
        'wish': wish,
        'users': wish.wished_by.all()
    }
    return render(request, 'wish/item.html', context)

def create(request):
    if request.method == "POST":
        errors = Wish.objects.validate(request.POST)

        if not errors:
            wish = Wish.objects.create_wish(request.POST, request.session["user_id"])
            return redirect(reverse('add_wish', args = (wish.id, )))

        flash_errors(request, errors)
        return redirect(reverse('wish/create_wish'))
    else:
        return render(request, 'wish/create.html')

def add_wish(request,wish_id):
    Wish.objects.add_wish(wish_id, request.session["user_id"])
    return redirect(reverse('main'))


def remove_wish(request,wish_id):
    Wish.objects.remove_wish(wish_id, request.session["user_id"])
    return redirect(reverse('main'))


def delete(request, wish_id):
    Wish.objects.delete_wish(wish_id)
    return redirect(reverse('main'))