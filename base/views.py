from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Team, Category
from django.db.models import Q
from .forms import TeamForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime

# Create your views here.
def home(request):
    q = request.GET.get('q')
    if q:
        q = '%'+ q + '%'
        teams = Team.objects.raw('SELECT * FROM base_team T, base_category C WHERE (T.name LIKE %s OR T.description LIKE %s OR C.name LIKE %s) AND T.category_id = C.id ' ,[q, q, q])
        # teams = Team.objects.filter(
        #     Q(category__name=q) |
        #     Q(name__icontains=q) |
        #     Q(description__icontains=q)
        # )
    else:
        teams = Team.objects.raw('SELECT * FROM base_team')
        #teams = Team.objects.all()
    #categories = Category.objects.all()
    categories = Category.objects.raw('SELECT * FROM base_category')
    context = {'teams': teams, 'categories': categories}
    return render(request, 'home.html', context)
    # return HttpResponse('Pocetna stranica')

def team(request, id):
    #team = Team.objects.get(id=id)
    team = Team.objects.raw('SELECT * FROM base_team WHERE id=%s',[id])
    #context = {'team': team}
    context = {'team': team[0]}
    return render(request, 'team.html', context)

@login_required(login_url='login')
def create_team(request):
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            #form.save()
            with connection.cursor() as cursor:
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                user_name = form.cleaned_data['user']
                user_id = User.objects.raw('SELECT * FROM auth_user WHERE username=%s', [user_name])[0].id
                category_name = form.cleaned_data['category']
                category_id = Category.objects.raw('SELECT * FROM base_category WHERE name=%s',[category_name])[0].id
                current_time_text = datetime.now().strftime('%y-%m-%d %H:%M:%S')
                cursor.execute("INSERT INTO base_team(name, description, updated, created,user_id,category_id) VALUES(%s,%s,%s,%s,%s,%s)", [name,description,current_time_text,current_time_text,user_id,category_id])
            return redirect('home')
    context = {'form': form}
    return render(request, 'team_form.html', context)

@login_required(login_url='login')
def edit_team(request, id):
    team = Team.objects.get(id=id)
    if request.user != team.user:
        return redirect('home')
    form = TeamForm(instance=team)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            #form.save()
            with connection.cursor() as cursor:
                name = form.cleaned_data['name']
                description = form.cleaned_data['description']
                user_name = form.cleaned_data['user']
                user_id = User.objects.raw('SELECT * FROM auth_user WHERE username=%s', [user_name])[0].id
                category_name = form.cleaned_data['category']
                category_id = Category.objects.raw('SELECT * FROM base_category WHERE name=%s',[category_name])[0].id
                current_time_text = datetime.now().strftime('%y-%m-%d %H:%M:%S')
                cursor.execute('UPDATE base_team SET name=%s, description=%s, user_id=%s, category_id=%s,updated=%s WHERE id=%s',[name, description, user_id, category_id, current_time_text, id])
            return redirect('home')
    context = {'form': form}
    return render(request, 'team_form.html', context)

@login_required(login_url='login')
def delete_team(request, id):
    #team = Team.objects.get(id=id)
    team = Team.objects.raw('SELECT * FROM base_team WHERE id=%s', [id][0])
    # if request.user != team.user:
    #     return redirect('home')
    if request.method == 'POST':
        #team.delete()
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM base_team WHERE id=%s', [id])
        return redirect('home')
    context = {'team': team}
    return render(request, 'team_delete.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
           user = User.objects.get(username=username)
        except:
           messages.error(request, 'User Does Not Exist.')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong Password.')
    return render(request, 'login_registration.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    return HttpResponse('Register')
