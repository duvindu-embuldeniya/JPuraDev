from django.urls import path
from . views import *

urlpatterns = [
    path('', home, name = 'home'), #profiles
    
    path('projects/', projects, name = 'projects'),
    path('project/<int:pk>/', project, name = 'project'),
    path('create-project', createProject, name = 'create-project'),
    path('update-project/<int:pk>/', updateProject, name = 'update-project'),
    path('delete-project/<int:pk>/', deleteProject, name = 'delete-project'),

    path('login/', login, name = 'login'),
    path('logout/', logout, name ='logout'),
    path('register/', register, name ='register'), 

    #navbar account tab
    path('profile/', userAccount, name = 'user-account'), 

    #navbar account edit
    path('edit-account/', editAccount, name = 'edit-account'), 
    
    #home single-developer's page click
    path('profile/<str:username>/', userProfile, name = 'user-profile'),

    path('delete/', deleteAccount, name = 'delete-account'),

    path('create-skill/', createSkill, name = 'create-skill'),
    path('update-skill/<int:pk>/', updateSkill, name = 'update-skill'),
    path('delete-skill/<int:pk>/', deleteSkill, name = 'delete-skill'),

    path('tag-create/<int:pk>/', createTag, name = 'tag-create'),
    path('tag-options/<int:pk>/', tagOptions, name = 'tag-options'),
    path('tag/<int:pk>/update/', updateTag, name = 'tag-update'),
    path('tag/<int:pk>/delete/', deleteTag, name = 'tag-delete'),

    path('inbox/', inbox, name = 'inbox'),
    path('messages/<int:pk>/', viewMessage, name = 'view-message'),
    path('create-message/<int:pk>/', createMessage, name = 'create-message'),

]