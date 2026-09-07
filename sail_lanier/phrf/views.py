from email.utils import formataddr

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from .forms import ContactForm
from .models import Cert, Profile
from .tables import CertTable, OfficerTable


def index(request):
    table = CertTable(Cert.valid.select_related('boat', 'boat__owner').order_by('boat__owner__last_name'))
    RequestConfig(request, paginate=False).configure(table)
    return render(request, 'phrf/certs.html', {'table': table, 'nav_bar': 'home'})


def rules(request):
    return render(request, 'phrf/rules.html', {'nav_bar': 'rules'})


def downloads(request):
    return render(request, 'phrf/documents.html', {'nav_bar': 'documents'})


def officers(request):
    table = OfficerTable(Profile.officers.select_related('user'))
    RequestConfig(request).configure(table)
    return render(request, 'phrf/table.html', {'table': table, 'nav_bar': 'officers'})


def contact(request, user_id=settings.PHRF_DEFAULT_OFFICER_ID):
    # the contact form should only allow contact with officers, not other users
    officer = Profile.officers.select_related('user').filter(pk=user_id).first()
    if officer is None:
        officer = Profile.objects.select_related('user').get(pk=settings.PHRF_DEFAULT_OFFICER_ID)

    error = None
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = EmailMessage(
                form.cleaned_data['subject'],
                form.cleaned_data['message'],
                formataddr((form.cleaned_data['name'], settings.DEFAULT_FROM_EMAIL)),
                [officer.user.email],
                reply_to=[form.cleaned_data['email']],
            )
            try:
                message.send()
            except ValueError:
                # Django raises ValueError for header injection; BadHeaderError
                # is deprecated and collapses into it in 7.0.
                error = 'Invalid header found.'
            else:
                return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'phrf/contact.html',
                  {'form': form, 'officer': officer, 'nav_bar': 'contact', 'error': error})


def contact_success(request):
    return render(request, 'phrf/contact_success.html')
