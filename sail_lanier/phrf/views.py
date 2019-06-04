from django.shortcuts import render
from django_tables2 import RequestConfig

from .models import Cert, Profile
from .tables import CertTable, OfficerTable


def index(request):
    table = CertTable(Cert.valid.all())
    RequestConfig(request, paginate=False).configure(table)
    context = {"table": table, "nav_bar": "home"}
    return render(request, "phrf/table.html", context=context)


def rules(request):
    context = {"nav_bar": "rules"}
    return render(request, "phrf/rules.html", context=context)


def downloads(request):
    context = {"nav_bar": "downloads"}
    return render(request, "phrf/downloads.html", context=context)


def officers(request):
    table = OfficerTable(Profile.officers.all())
    RequestConfig(request).configure(table)
    context = {"table": table, "nav_bar": "officers"}
    return render(request, "phrf/table.html", context=context)
