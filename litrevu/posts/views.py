from itertools import chain
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from authentication.models import User
from subscription.models import UserFollows

from .models import Review, Ticket
from .forms import TicketForm  
from .forms import ReviewForm
from django.db.models import Count

from django.db.models import Q

@login_required
def flows(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    followed_tickets = Ticket.objects.filter(user__in=followed_users)
    
    # Annoter les tickets avec le nombre de reviews
    tickets = (user_tickets | followed_tickets).annotate(
        review_count=Count('review')
    )

    ticket_reviews = Review.objects.filter(ticket__in=tickets).select_related('ticket')
        
    combined_list = sorted(chain(tickets, ticket_reviews), key=lambda x: x.time_created, reverse=True)
    
    for item in combined_list:
        if isinstance(item, Ticket):
            item.already_responded = item.review_count > 0
        elif isinstance(item, Review):
            # Le ticket de cette review a déjà au moins une review (cette review elle-même)
            item.ticket.already_responded = True

    context = {
        'combined_list': combined_list,
        'is_flows_page': True,
    }
    return render(request, 'pages/flows.html', context)


@login_required
def posts(request):
    user_tickets = Ticket.objects.filter(user=request.user)
    
    # Récupérer les reviews liées aux tickets de l'utilisateur
    ticket_reviews = Review.objects.filter(ticket__in=user_tickets)
    
    # Récupérer les reviews créées par l'utilisateur (ajout de cette ligne)
    user_reviews = Review.objects.filter(user=request.user)
    
    # Combiner toutes les reviews (sans doublons)
    all_reviews = (ticket_reviews | user_reviews).distinct()
    
    combined_list = sorted(
        chain(all_reviews, user_tickets),
        key=lambda x: x.time_created,
        reverse=True
    )
    context = {'combined_list': combined_list}
    print(combined_list)
    return render(request, 'pages/posts.html', context)


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
def remove_review(request, review_id):
    if request.method == 'POST':
        review = Review.objects.get(pk=review_id)
        review.delete()

    return redirect('posts')


@login_required
def remove_ticket_and_reviews(request, ticket_id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket.delete()

    return redirect('posts')


@login_required
def create_review(request, ticket_id=None):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
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

    context = {
        'ticket_form': ticket_form,
        'review_form': review_form
    }
    return render(request, 'formularies/create_review.html', context)


@login_required
def modify_response_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('posts')
    else:
        review_form = ReviewForm(instance=review)

    context = {
        'review_form': review_form,
        'review': review
    }
    return render(request, 'formularies/create_response_review.html', context)

    

@login_required
def create_response_review(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('flows')
    else:
        review_form = ReviewForm()

    context = {
        'review_form': review_form,
        'ticket': ticket
    }
    return render(request, 'formularies/create_response_review.html', context)

@login_required
def modify_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id, user=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    else:
        form = TicketForm(instance=ticket)

    context = {
        'form': form,
        'ticket': ticket
    }
    return render(request, 'formularies/create_ticket.html', context)


@login_required
def modify_review(request):
    return render(request, 'posts/modify_review.html')



