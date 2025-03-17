from django.forms import ModelForm
from . models import Project, Profile, Skill, Review, Message, Tag
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description', 'source_link']

        # widgets = {
        
        #     'tags' : forms.CheckboxSelectMultiple(),
        # }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
            
        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add title'})
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})





class UserRegistrationForm(UserCreationForm):
    class Meta:
        email = forms.EmailField(required=True)
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        #labels = {
            #'email': 'Emaillll', #appear
            #'password1': 'Password 1st', #not support as theay are default

        #}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already taken!')
        return email



    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
            
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})





class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'location', 'intro', 'bio', 'image']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
            
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})





class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
            
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})





class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
    
        labels = {
            'value': 'Place your vote',   
            'body': 'Add a comment with a your vote',
        }


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
                
        self.fields['value'].widget.attrs.update({'class': 'input'})
        self.fields['body'].widget.attrs.update({'class': 'input', 'placeholder': 'Only one comment is allowed per project. Once submitted, it cannot be changed!'})





class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
                
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})




class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
                
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})