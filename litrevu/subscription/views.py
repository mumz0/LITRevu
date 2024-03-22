from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def follows(request):
    return render(request, 'subscription/follows.html')
