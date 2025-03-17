from django.db.models import Q
from . models import Profile, Project, Tag
 
def searchProfiles(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains = q)
    )

    return profiles,q


# distinct().filter()
# 1:m
# m:m


def searchProjects(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    tags = Tag.objects.filter(name__icontains = q)
    projects = Project.objects.distinct().filter(
        Q(title__icontains = q)|
        Q(tag__in = tags)
    )

    return projects, q