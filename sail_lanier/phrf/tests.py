from django.contrib.auth.models import Group, User
from django.test import TestCase

from .models import Profile
from .tables import OfficerTable


class TestTables(TestCase):
    def setUp(self):
        club_rep = Group.objects.create(name="Club Representative")
        member_at_large = Group.objects.create(name="Member at Large")
        crep = User.objects.create(username="crep", first_name="Club", last_name="Rep", email="club@rep.com")
        crep.groups.set([club_rep])
        Profile.objects.create(user=crep, club=0)
        mlarge = User.objects.create(username="mlarge", first_name="Large", last_name="Member", email="lrg@member.com")
        mlarge.groups.set([member_at_large])
        Profile.objects.create(user=mlarge, club=2)

    def test_officers(self):
        table = OfficerTable(Profile.officers.select_related("user").all())
        table.order_by = "-group"
        for i in table.as_values():
            self.assertIs(type(i), list)
