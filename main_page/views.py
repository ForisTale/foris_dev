from django.shortcuts import render


def home_page(request):
    return render(request, "main_page/home.html")


def about_me(request):
    return render(request, "main_page/about_me.html")
