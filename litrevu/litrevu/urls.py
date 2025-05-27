"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView

import authentication.views
import posts.views
import subscription.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/auth.html',
        redirect_authenticated_user=True),
        name='auth'),
    path('signup/', authentication.views.signup, name='signup'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('flows/', posts.views.flows, name='flows'),
    path('posts/', posts.views.posts, name='posts'),
    path('create_ticket/', posts.views.create_ticket, name='create_ticket'),
    path('create_review/', posts.views.create_review, name='create_review'),
    path('create_review/<int:ticket_id>/', posts.views.create_review, name='create_review'),
    path('modify_response_review/<int:review_id>/', posts.views.modify_response_review, name='modify_response_review'),
    path('create_response_review/<int:ticket_id>/', posts.views.create_response_review, name='create_response_review'),
    path('modify_ticket/<int:ticket_id>/', posts.views.modify_ticket, name='modify_ticket'),
    path('modify_review/<int:review_id>/', posts.views.modify_review, name='modify_review'),
    path('follows/', subscription.views.follows_list, name='follows'),
    path('add_follower/', subscription.views.add_follower, name='add_follower'),
    path('remove_follower/<int:user_id>/', subscription.views.remove_follower, name='remove_follower'),
    path('remove_ticket_and_reviews/<int:ticket_id>/', posts.views.remove_ticket_and_reviews, name='remove_ticket_and_reviews'),
    path('remove_review/<int:review_id>/', posts.views.remove_review, name='remove_review'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)