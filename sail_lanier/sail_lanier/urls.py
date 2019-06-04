from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url="phrf/", permanent=False)),
    path('admin/', admin.site.urls),
    path('phrf/', include("phrf.urls")),
]
