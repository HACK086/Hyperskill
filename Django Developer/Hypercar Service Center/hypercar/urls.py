from django.urls import path
from django.views.generic.base import RedirectView
from tickets.views import WelcomeView, MenuView, TicketView, OperatorView, NextView


urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view()),
    path('get_ticket/<str:link>', TicketView.as_view()),
    path('processing', OperatorView.as_view()),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('next', NextView.as_view()),
    path('next/', RedirectView.as_view(url='/next')),
]