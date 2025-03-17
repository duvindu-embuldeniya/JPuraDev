from django.shortcuts import render
from django.shortcuts import render, redirect
from . models import Project, Review, Tag, Profile, Skill, Message
from . forms import (ProjectForm, UserRegistrationForm, 
                     ProfileForm,SkillForm, ReviewForm, 
                     MessageForm, TagForm)

from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . utils import searchProfiles, searchProjects
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def home(request): #profiles
    profiles,q = searchProfiles(request)  

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(profiles, results)

    try: 
        profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    context = {'profiles': profiles, 'q':q, 'paginator': paginator}
    return render(request, 'home/index.html', context)



def register(request):
    page = 'register'
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'Account created successfully!')
            auth.login(request, new_user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error occurred during registration!")
    context = {'page':page, 'form':form}
    return render(request, 'home/login_register.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username = username, password = password)
        if auth_user is not None:
            auth.login(request, auth_user)
            messages.success(request, "Successfully logged in!")
            return redirect(request.GET.get('next') if request.GET.get('next') else 'home')
        else:
            messages.error(request, "Username or password incorrect!")
    return render(request, 'home/login_register.html')



def logout(request):
    if not(request.user.is_authenticated):
        messages.info(request, "You are not logged-in!")
        return redirect('home')
    auth.logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')



def projects(request):
    projects,q = searchProjects(request)

    page = request.GET.get('page')
    results = 2
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.page_range
        projects = paginator.page(page)

    context = {'projects': projects, 'q': q}
    return render(request, 'home/projects.html', context)



def project(request, pk):
    project = Project.objects.get(id = pk)
    tags = project.tag_set.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user 
            review.project = project
            review.save()
            messages.success(request, "Review added successfully!")
    
            #update project vote values...
            project.getVoteCount

            return redirect('project', pk = project.pk)

    context = {'project': project, 'tags': tags, 'form': form}
    return render(request, 'home/project_single.html', context)



@login_required
def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('user-account')
    context = {'form':form}
    return render(request, 'home/project_create.html', context)



@login_required
def updateProject(request, pk):
    project = Project.objects.get(id = pk)
    if project.owner != request.user:
        return HttpResponse("<h1>You are not allowed here!")
    form = ProjectForm(instance = project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('user-account')
    context = {'form': form}
    return render(request, 'home/project_update.html', context)



@login_required
def deleteProject(request, pk):
    project = Project.objects.get(id = pk)
    if project.owner != request.user:
        return HttpResponse("<h1>You are not allowed here!")
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('user-account')
    context = {'obj': project}
    return render(request, 'home/project_delete.html', context)



def userProfile(request, username): #home single-developer's page click
    profile = Profile.objects.get(username = username)
    skills = profile.user.skill_set.all()
    projects = profile.user.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'home/user_profile.html', context)



@login_required
def userAccount(request): #navbar account
    owner = request.user
    skills = owner.skill_set.all()
    projects = owner.project_set.all()
    context = {'owner': owner, 'skills': skills, 'projects': projects}
    return render(request, 'home/profile_view.html', context)



@login_required
def editAccount(request): #navbar account edit
    form = ProfileForm(instance = request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated successfully!")
            return redirect('user-account')
    context = {'form': form}
    return render(request, 'home/profile_edit.html', context)



@login_required
def deleteAccount(request):
    obj = request.user
    if obj != request.user:
        return HttpResponse('<h1>You are not allowed here!')
    context = {'obj': obj}
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "You deleted successfully!")
        return redirect('home')
    return render(request, 'home/profile_delete.html', context)

@login_required
def createSkill(request):
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user
            skill.save()
            messages.success(request, "Skill added successfully!")
            return redirect('user-account')
    context = {'form': form}
    return render(request, 'home/skill_create.html', context)



@login_required
def updateSkill(request, pk):
    skill = Skill.objects.get(pk=pk)
    if skill.owner != request.user:
        return HttpResponse("<h1>You are not allowed here!</h1>")
    form = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect('user-account')
    context = {'form': form}
    return render(request, 'home/skill_update.html', context)



@login_required
def deleteSkill(request, pk):
    skill = Skill.objects.get(pk=pk)
    if skill.owner != request.user:
        return HttpResponse("<h1>You are not allowed here!</h1>")
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill deleted successfully!")
        return redirect('user-account')
    context = {'obj':skill}
    return render(request, 'home/skill_delete.html', context)



@login_required
def inbox(request):
    msgs = request.user.receiver.all()
    count = msgs.count()
    unread_count = msgs.filter(is_read = False).count()
    context = {'msgs':msgs, 'unread_count':unread_count, 'count':count}
    return render(request, 'home/message_inbox.html', context)



@login_required
def viewMessage(request, pk):
    msg = Message.objects.get(pk = pk)
    if msg.receiver != request.user:
        return HttpResponse('<h1>You are not allowed here!')
    if msg.is_read == False:
        msg.is_read = True
        msg.save()
    context = {'msg':msg}
    return render(request, 'home/message_view.html', context)



@login_required
def createMessage(request, pk):
    recepient = User.objects.get(pk = pk)
    sender = request.user
    receiver = recepient
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.name = sender.profile.name
            msg.email = sender.email
            msg.sender = sender
            msg.receiver = receiver
            msg.save()
            messages.success(request, "Message sent successfully!")
            return redirect('user-profile', username = recepient.username)
    context = {'form':form, 'recepient':recepient}
    return render(request, 'home/message_create.html', context)



@login_required
def createTag(request, pk):
    project = Project.objects.get(pk=pk)
    form = TagForm()
    context = {'form':form}
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.project = project
            tag.save()
            messages.success(request, "Tag added successfully!")
            return redirect('user-account')
    return render(request, 'home/tag_create.html', context)



@login_required
def updateTag(request, pk):
    tag = Tag.objects.get(pk=pk)
    if tag.project.owner != request.user:
        return HttpResponse('<h1>You are not allowed here!')
    form = TagForm(instance = tag)
    if request.method == 'POST':
        form = TagForm(request.POST, instance = tag)
        if form.is_valid():
            tag = form.save()
            messages.success(request, "Tag updated successfully!")
            return redirect('user-account')
    context = {'tag': tag, 'form': form}
    return render(request, 'home/tag_update.html', context)



@login_required
def deleteTag(request, pk):
    tag = Tag.objects.get(pk=pk)
    if tag.project.owner != request.user:
        return HttpResponse('<h1>You are not allowed here!')
    if request.method == 'POST':
        tag.delete()
        messages.success(request, "Tag deleted successfully!")
        return redirect('user-account')
    context = {'tag': tag}
    return render(request, 'home/tag_delete.html', context)



@login_required
def tagOptions(request, pk):
    tag = Tag.objects.get(pk=pk)
    if tag.project.owner != request.user:
        return HttpResponse('<h1>You are not allowed here!')
    if tag.project.owner != request.user:
        return HttpResponse('<h1>You are not allowed here!')
    context = {'tag': tag}
    return render(request, 'home/tag_option.html', context)