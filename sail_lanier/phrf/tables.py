from django_tables2 import tables

from .models import Cert, Profile


class CertTable(tables.Table):
    owner_name = tables.Column(order_by='boat__owner__last_name')
    boat_name = tables.Column(order_by='boat__boat_name')
    boat_type = tables.Column(order_by='boat__boat_type')
    sail_number = tables.Column(order_by='boat__sail_number')
    adjusted_rating = tables.Column(attrs={'td': {'class': 'font-weight-bold'}})

    class Meta:
        fields = ['owner_name', 'boat_name', 'boat_type', 'sail_number', 'base_rating', 'adjusted_rating',
                  'non_spin_rating', 'expiration_date']
        model = Cert


class OfficerTable(tables.Table):
    name = tables.Column(order_by=('user__first_name', 'user__last_name'),
                         linkify=('contact', {'user_id': tables.Accessor('user__id')}))
    group = tables.Column(order_by='user__groups', verbose_name='Position')

    class Meta:
        fields = ['name', 'group', 'club']
        model = Profile
