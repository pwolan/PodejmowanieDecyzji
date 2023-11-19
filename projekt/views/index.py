from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    groupnames = request.user.groups.all()
    context = {
        'user': request.user,
        'groupnames': groupnames
       }
    return render(request, "projekt/index.html", context)



