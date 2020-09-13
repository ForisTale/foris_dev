from django.shortcuts import render, redirect
from django.core.mail import send_mail
from the_elder_commands.utils import MessagesSystem
from smtplib import SMTPException


def home_page(request):
    return render(request, "main_page/home.html")


def about_me(request):
    return render(request, "main_page/about_me.html")


def contact(request):
    messages = MessagesSystem(request)
    if request.method == "POST":
        try:
            send_mail(request.POST.get("subject"), request.POST.get("message"), request.POST.get("email"),
                      ["foris.dev@gmail.com"])
            messages.append_contact("Message was sent!")
        except SMTPException:
            messages.append_contact("Something went wrong! \nPlease try a different method of contact.")
        return redirect("main_page:contact")

    return render(request, "main_page/contact.html", {"messages": messages.pop_contact()})
