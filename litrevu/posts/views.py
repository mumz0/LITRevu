from itertools import chain
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket
from .forms import TicketForm  
from .forms import ReviewForm
from django.db.models import Count

@login_required
def flows(request):

    # tickets = Ticket.objects.all()
    tickets_without_review = Ticket.objects.annotate(
    num_reviews=Count('review')
    ).filter(num_reviews=0)
    reviews = Review.objects.select_related('ticket').all()

    combined_list = sorted(
        chain(tickets_without_review, reviews),
        key=lambda x: x.time_created,
        reverse=True
    )

    context = {
        'combined_list': combined_list,
    }
    print(combined_list)
    return render(request, 'pages/flows.html', context)


@login_required
def posts(request):
    return render(request, 'pages/posts.html')

@login_required
def create_ticket(request):
    return render(request, 'formularies/create_ticket.html')

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            # print("form", form)
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('posts')
    else:
        form = TicketForm()
    return render(request, 'formularies/create_ticket.html', {'form': form})

@login_required
def create_review(request):
    return render(request, 'formularies/create_review.html')

@login_required
def create_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        print(request.POST)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('posts')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request, 'formularies/create_review.html', context)

@login_required
def create_ticket_review(request):
    return render(request, 'formularies/create_ticket_review.html')

@login_required
def modify_ticket(request):
    return render(request, 'posts/modify_ticket.html')

@login_required
def modify_review(request):
    return render(request, 'posts/modify_review.html')



