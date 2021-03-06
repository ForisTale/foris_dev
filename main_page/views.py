from django.shortcuts import render, redirect
from django.core.mail import send_mail
from the_elder_commands.utils.check_recaptcha import check_recaptcha
from the_elder_commands.utils.messages_system import MessagesSystem
from django.conf import settings
from smtplib import SMTPException


def home_page(request):
    return render(request, "main_page/home.html")


def about_me(request):
    return render(request, "main_page/about_me.html")


def contact(request):
    messages = MessagesSystem(request)
    if request.method == "POST":

        send_contact_email(request)

        return redirect("main_page:contact")

    return render(request, "main_page/contact.html", {"messages": messages.pop_contact(),
                                                      "site_key": settings.RECAPTCHA_SITE_KEY})


@check_recaptcha("contact")
def send_contact_email(request):
    messages = MessagesSystem(request)
    try:
        email_message = f"Email: {request.POST.get('email')} \nMessage: {request.POST.get('message')}"
        send_mail(request.POST.get("subject"), email_message, "",
                  ["foris.dev@gmail.com"])
        messages.append_contact("Message was sent!")
    except SMTPException:
        messages.append_contact("Something went wrong! \nPlease try a different method of contact.")
