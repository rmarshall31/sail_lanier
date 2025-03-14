from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from . import settings as app_settings
from .forms import ContactForm
from .models import Cert, Profile, User
from .tables import CertTable, OfficerTable


def index(request):
    table = CertTable(
        Cert.valid.select_related('boat', 'boat__owner').all().order_by('boat__owner__last_name'))
    RequestConfig(request, paginate=False).configure(table)
    context = {'table': table, 'nav_bar': 'home'}
    return render(request, 'phrf/certs.html', context=context)


def rules(request):
    context = {'nav_bar': 'rules'}
    return render(request, 'phrf/rules.html', context=context)


def downloads(request):
    context = {'nav_bar': 'documents'}
    return render(request, 'phrf/documents.html', context=context)


def officers(request):
    table = OfficerTable(Profile.officers.select_related('user').all())
    RequestConfig(request).configure(table)
    context = {'table': table, 'nav_bar': 'officers'}
    return render(request, 'phrf/table.html', context=context)


def contact(request, user_id=app_settings.DEFAULT_USER_ID):
    # the contact form should only allow contact with officers, not other users
    user = Profile.officers.filter(pk=user_id).select_related('user').first()
    if user is None:
        user = Profile.objects.select_related('user').get(pk=app_settings.DEFAULT_USER_ID)

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                email = EmailMessage(subject, message,
                                     '"{name}" <{email}>'.format(name=name, email=app_settings.EMAIL_FROM),
                                     [User.objects.get(pk=user.user_id).email], reply_to=[email])
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_success')
    context = {'form': form, 'user': user, 'nav_bar': 'contact'}
    return render(request, 'phrf/contact.html', context=context)


def contact_success(request):
    return render(request, 'phrf/contact_success.html')
