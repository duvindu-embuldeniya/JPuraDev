from django.db import models
from django.contrib.auth.models import User
# import uuid

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'project/', default='project/default.jpg', null=True, blank=True)
    description = models.TextField()
    source_link = models.CharField(max_length=200, null=True, blank=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    # id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total']

    @property
    def getVoteCount(self):
        reviews= self.review_set.all()
        upvotes = reviews.filter(value = 'Up Vote')

        total_votes = reviews.count()
        ratio = (upvotes.count() / reviews.count()) * 100

        self.vote_total = total_votes
        self.vote_ratio = ratio

        self.save()
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('reviewer__id', flat = True)
        return queryset

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return '/images/project/default.jpg'
        


class Review(models.Model):
    VOTE_TYPE = (
        ('Up Vote', 'Up Vote'),
        ('Down Vote', 'Down Vote'),
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField()
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['reviewer', 'project']

    def __str__(self):
        return f"{self.value}"


class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True) 
    location = models.CharField(max_length=200, null=True)
    intro = models.CharField(max_length=200, null = True)
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to = 'profile/', default='profile/default.png', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return '/images/profile/default.png'


class Skill(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}" 


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['is_read','-created']

        #boolean fields ascending order.. means all False values first... 
