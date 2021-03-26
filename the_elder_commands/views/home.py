from django.shortcuts import render


def home_view(request):
    return render(request, "the_elder_commands/home.html")