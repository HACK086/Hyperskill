from django.views import View
from django.shortcuts import render, redirect
from django.http.response import HttpResponse


def proc(serv):
    global queue
    time_dict = {'change_oil': 2,
                 'inflate_tires': 5,
                 'diagnostic': 30}
    number, time = 0, 0
    if serv == 'change_oil':
        time = queue[serv] * time_dict[serv]
        queue[serv] += + 1
        ticket[serv].append(max(max(ticket['change_oil']), max(ticket['inflate_tires']), max(ticket['diagnostic'])) + 1)
        return queue[serv], time
    elif serv == 'inflate_tires':
        time += queue[serv] * time_dict[serv] + queue['change_oil'] * time_dict['change_oil']
        queue[serv] += 1
        ticket[serv].append(max(max(ticket['change_oil']), max(ticket['inflate_tires']), max(ticket['diagnostic'])) + 1)
        return queue[serv], time
    for i in queue:
        time += queue[i] * time_dict[i]
        number += queue[i]
    ticket[serv].append(max(max(ticket['change_oil']), max(ticket['inflate_tires']), max(ticket['diagnostic'])) + 1)
    queue[serv] += 1
    return number, time


def next_():
    global ticket, queue
    if len(ticket['change_oil']) > 1:
        queue['change_oil'] -= 1
        return ticket['change_oil'].pop(1)
    elif len(ticket['inflate_tires']) > 1:
        queue['inflate_tires'] -= 1
        return ticket['inflate_tires'].pop(1)
    elif len(ticket['diagnostic']) > 1:
        queue['diagnostic'] -= 1
        return ticket['diagnostic'].pop(1)
    return 0


ticket = {'change_oil': [0],
          'inflate_tires': [0],
          'diagnostic': [0]}
queue = {'change_oil': 0,
         'inflate_tires': 0,
         'diagnostic': 0}
last = 0


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class Menu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/index.html')


class GetTickets(View):
    def get(self, request, *args, **kwargs):
        n, t = proc(args[0])
        return render(request, 'tickets/tickets.html', context={'number': n, 'time': t})


class NextPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', context={'queue': last})


class OperatorMenu(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/operator.html', context={'queue': queue})

    def post(self, request, *args, **kwargs):
        global last
        last = next_()
        return render(request, 'tickets/next.html', context={'queue': last})
