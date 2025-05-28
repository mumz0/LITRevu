from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from authentication.models import User
from subscription.models import UserFollows
from subscription import forms

from django.contrib import messages


@login_required
def follows_list(request):
    current_user = request.user

    # Récupérer les personnes que l'utilisateur suit
    following = current_user.following.all().select_related("followed_user")

    # Récupérer les followers de l'utilisateur
    followers = current_user.followed_by.all().select_related("user")

    # Convertir les QuerySets en listes d'utilisateurs
    following_users = [relationship.followed_user for relationship in following]
    follower_users = [relationship.user for relationship in followers]

    context = {
        "following": following_users,
        "followers": follower_users,
    }

    return render(request, "subscription/follows.html", context)


@login_required
def add_follower(request):
    if request.method == "GET":
        search_form = forms.SearchForm(request.GET)
        if search_form.is_valid():
            search_query = search_form.cleaned_data["query"]
            try:
                user_to_follow = User.objects.get(username=search_query)

                if user_to_follow == request.user:
                    messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
                else:
                    if UserFollows.objects.filter(
                        user=request.user, followed_user=user_to_follow
                    ).exists():
                        messages.warning(request, f"Vous suivez déjà {search_query}.")
                    else:
                        user_follow = UserFollows(
                            user=request.user, followed_user=user_to_follow
                        )
                        user_follow.save()
                        messages.success(
                            request, f"Vous suivez maintenant {search_query}."
                        )

            except User.DoesNotExist:
                messages.error(request, f"L'utilisateur '{search_query}' n'existe pas.")

    return redirect("follows")


@login_required
def remove_follower(request, user_id):
    if request.method == "POST":
        user_follow = UserFollows.objects.get(
            user=request.user, followed_user=User.objects.get(pk=user_id)
        )
        user_follow.delete()

    return redirect("follows")
