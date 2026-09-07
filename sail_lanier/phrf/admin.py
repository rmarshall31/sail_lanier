import csv
from datetime import date

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from django.urls import path

from .models import Boat, Cert, CertRequest, Profile, TransferRequest

admin.site.site_header = 'Sail Lanier Admin'
admin.site.index_template = 'phrf/admin_index.html'
admin.site.register(CertRequest)
admin.site.register(TransferRequest)


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ('boat_name', 'sail_number', 'boat_type', 'owner__last_name')
    list_select_related = ('owner',)
    search_fields = ('boat_name', 'boat_type', 'owner__first_name', 'owner__last_name')


class _CsvEcho:
    """File-like target that returns whatever is written, for csv.writer streaming."""

    def write(self, value):
        return value


CERT_REPORT_COLUMNS = (
    'boat__owner__first_name', 'boat__owner__last_name', 'boat__boat_name', 'boat__boat_type',
    'base_rating', 'adjusted_rating', 'non_spin_rating',
    'expiration_date', 'comments',
)

# headers drop the relation prefix so the CSV reads as a flat cert/boat/owner record
CERT_REPORT_HEADERS = tuple(column.rpartition('__')[2] for column in CERT_REPORT_COLUMNS)


@admin.register(Cert)
class CertAdmin(admin.ModelAdmin):
    change_list_template = 'admin/phrf/cert/change_list.html'
    list_display = ('boat__boat_name', 'boat__boat_type', 'boat__owner__last_name', 'base_rating',
                    'adjusted_rating', 'expiration_date')
    list_select_related = ('boat', 'boat__owner')
    search_fields = ('boat__boat_name', 'boat__boat_type', 'boat__owner__last_name')

    def get_urls(self):
        return [
            path(
                'report.csv',
                self.admin_site.admin_view(self.cert_report_csv),
                name='phrf_cert_report_csv',
            ),
        ] + super().get_urls()

    def cert_report_csv(self, request):
        rows = (
            Cert.objects
            .order_by(
                '-expiration_date',
                'boat__owner__last_name',
                'boat__owner__first_name',
                'boat__boat_name',
            )
            .values_list(*CERT_REPORT_COLUMNS)
        )

        writer = csv.writer(_CsvEcho())

        def stream():
            yield writer.writerow(CERT_REPORT_HEADERS)
            for row in rows.iterator():
                yield writer.writerow(row)

        filename = f'phrf_cert_report_{date.today().isoformat()}.csv'
        response = StreamingHttpResponse(stream(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
