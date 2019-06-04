from django_tables2 import tables

from .models import Cert, Profile


class CertTable(tables.Table):
    owner_name = tables.columns.Column(order_by="boat.owner.last_name")
    boat_name = tables.columns.Column(order_by="boat.boat_name")
    boat_type = tables.columns.Column(order_by="boat.boat_type")
    sail_number = tables.columns.Column(order_by="boat.sail_number")
    adjusted_rating = tables.columns.Column(attrs={"td": {"class": "font-weight-bold"}})

    class Meta:
        fields = ["owner_name", "boat_name", "boat_type", "sail_number", "base_rating", "adjusted_rating",
                  "non_spin_rating", "expiration_date"]
        model = Cert


class OfficerTable(tables.Table):
    name = tables.columns.Column(order_by=("user.first_name", "user.last_name"))
    group = tables.columns.Column(order_by="user.group", verbose_name="Position")
    email = tables.columns.Column(order_by="user.email")

    class Meta:
        fields = ["name", "group", "club", "email"]
        model = Profile
