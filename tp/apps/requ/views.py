from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from .forms import LoginForm
from .models import Request, Comment
from django.http import Http404, HttpResponseRedirect, HttpResponse
from datetime import datetime


def index(request):
    return render(request, 'requ/index.html', {'is_auth': request.user.is_authenticated})


def comment(request, id):
    try:
        a = Request.objects.get(id=id)
    except:
        raise Http404("Заявка не найдена!")

    c = Comment(text=request.POST['text'], author=request.user, request=a)
    c.save()
    return HttpResponseRedirect('/' + str(id))


def detail(request, id):
    try:
        req = Request.objects.get(id=id)
        user_ = request.user
        if user_.groups.filter(name="sysadm").exists() or user_.is_superuser or user_ == req.author:
            comments = Comment.objects.filter(request=req)
        else:
            return HttpResponse("Недостаточно прав!")
    except:
        raise Http404("Заявка не найдена!")
    return render(request, 'requ/detail.html', {'req': req, 'comments': comments})


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user_ = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user_ is not None:
                if user_.is_active:
                    login(request, user_)
                    if user_.groups.filter(name='user').exists():
                        return HttpResponseRedirect('/user/')
                    if user_.groups.filter(name='sysadm').exists():
                        return HttpResponseRedirect('/sysadmin/')
                else:
                    return render(request, 'requ/login.html', {'error': 'disabled'})
            else:
                return render(request, 'requ/login.html', {'error': 'invalid'})
    return render(request, 'requ/login.html', {'is_auth': request.user.is_authenticated,
                                               'user': request.user})


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def user(request):
    reqs = Request.objects.order_by('-pub_date').filter(author=request.user)
    if request.user.groups.filter(name='user').exists() or request.user.is_superuser:
        return render(request, 'requ/user.html', {'reqs': reqs})
    else:
        return HttpResponse('Недостаточно прав')


def admin(request):
    reqs = Request.objects.order_by('-pub_date').filter(is_solved=False)
    if request.user.groups.filter(name='sysadm').exists() or request.user.is_superuser:
        return render(request, 'requ/admin.html', {'reqs': reqs})
    else:
        return HttpResponse('Недостаточно прав')


def new_request(request):
    if request.method == "POST":
        r = Request(text=request.POST['text'], author=request.user, is_solved=False,
                    pub_date=datetime.now())
        r.save()
        print(r)
        return HttpResponseRedirect('/back/')
    else:
        return render(request, "requ/new_request.html", {'is_auth': request.user.is_authenticated})


def profile(request):
    user_ = request.user
    if user_.is_authenticated:
        if user_.groups.filter(name="sysadm").exists():
            status = "Системный администратор"
        elif user_.groups.filter(name="user").exists():
            status = "Пользователь"
        elif user_.is_superuser:
            status = "Админ"
        else:
            status = "Другое"
        return render(request, 'requ/profile.html', {'user': user_, 'status': status})
    else:
        return HttpResponseRedirect('/login/')


def solved(request, id):
    a = Request.objects.get(id=id)
    a.solver = request.user
    a.is_solved = True
    a.save()
    return HttpResponseRedirect('/' + str(id))


def unsolved(request, id):
    a = Request.objects.get(id=id)
    a.solver = None
    a.is_solved = False
    a.save()
    return HttpResponseRedirect('/' + str(id))


def back(request):
    user_ = request.user
    if user_.groups.filter(name='user').exists():
        return HttpResponseRedirect('/user/')
    elif user_.groups.filter(name='sysadm').exists():
        return HttpResponseRedirect('/sysadmin/')
    elif user_.is_superuser:
        return HttpResponseRedirect('/sysadmin/')
    else:
        return HttpResponseRedirect('/login/')
