from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', Menu.as_view()),
    re_path(r'get_ticket/(change_oil|inflate_tires|diagnostic)/', GetTickets.as_view()),
    path('processing', OperatorMenu.as_view()),
    path('next/', NextPage.as_view())
]