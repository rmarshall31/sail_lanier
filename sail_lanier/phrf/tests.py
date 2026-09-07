from datetime import date

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Boat, Cert, Profile
from .tables import CertTable, OfficerTable


class TestOfficerTable(TestCase):
    def setUp(self):
        club_rep = Group.objects.create(name='Club Representative')
        member_at_large = Group.objects.create(name='Member at Large')
        crep = User.objects.create(username='crep', first_name='Club', last_name='Rep', email='club@rep.com')
        crep.groups.set([club_rep])
        Profile.objects.create(user=crep, club=0)
        mlarge = User.objects.create(username='mlarge', first_name='Large', last_name='Member', email='lrg@member.com')
        mlarge.groups.set([member_at_large])
        Profile.objects.create(user=mlarge, club=2)

    def test_rows(self):
        table = OfficerTable(Profile.officers.select_related('user'))
        self.assertEqual(list(table.as_values()), [
            ['Name', 'Position', 'Club'],
            ['Large Member', 'Member at Large', 'LLSC'],
            ['Club Rep', 'Club Representative', 'None'],
        ])

    def test_officer_in_two_roles_is_listed_once(self):
        crep = User.objects.get(username='crep')
        crep.groups.add(Group.objects.get(name='Member at Large'))
        self.assertEqual(Profile.officers.count(), 2)


class TestCertTable(TestCase):
    def test_columns_reach_through_the_boat_relation(self):
        owner = User.objects.create(username='skipper', first_name='Ann', last_name='Skipper')
        boat = Boat.objects.create(owner=owner, boat_name='Kestrel', boat_type='J/24', sail_number='123')
        Cert.objects.create(boat=boat, base_rating=170, adjusted_rating=168,
                            expiration_date=date(2099, 12, 31), application_date=date(2020, 1, 1))

        table = CertTable(Cert.valid.all())
        self.assertEqual(list(table.as_values()), [
            ['Owner name', 'Boat name', 'Boat type', 'Sail number',
             'Base rating', 'Adjusted rating', 'Non spin rating', 'Expiration date'],
            ['Skipper', 'Kestrel', 'J/24', '123', 170, 168, None, '2099-12-31'],
        ])


class TestCertAdmin(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser('root', 'root@example.com', 'pw'))
        owner = User.objects.create(username='skipper', first_name='Ann', last_name='Skipper')
        boat = Boat.objects.create(owner=owner, boat_name='Kestrel', boat_type='J/24', sail_number='123')
        Cert.objects.create(boat=boat, base_rating=170, adjusted_rating=168,
                            expiration_date=date(2099, 12, 31), application_date=date(2020, 1, 1))

    def test_changelists_render_related_columns(self):
        for name in ('admin:phrf_boat_changelist', 'admin:phrf_cert_changelist'):
            with self.subTest(changelist=name):
                self.assertContains(self.client.get(reverse(name)), 'Skipper')

    def test_index_links_the_report(self):
        self.assertContains(self.client.get(reverse('admin:index')),
                            reverse('admin:phrf_cert_report_csv'))

    def test_report_csv(self):
        response = self.client.get(reverse('admin:phrf_cert_report_csv'))
        body = b''.join(response.streaming_content).decode()
        self.assertEqual(body.splitlines(), [
            'first_name,last_name,boat_name,boat_type,base_rating,adjusted_rating,non_spin_rating,'
            'expiration_date,comments',
            'Ann,Skipper,Kestrel,J/24,170,168,,2099-12-31,',
        ])


class TestPages(TestCase):
    def setUp(self):
        chairman = Group.objects.create(name='Chairman')
        officer = User.objects.create(pk=settings.PHRF_DEFAULT_OFFICER_ID, username='chair', first_name='Ada',
                                      last_name='Chair', email='chair@example.com')
        officer.groups.set([chairman])
        Profile.objects.create(user=officer, club=1)

    def test_every_page_renders(self):
        for name in ('index', 'rules', 'documents', 'officers', 'contact', 'contact_success'):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_contact_addresses_the_officer_named_in_the_url(self):
        url = reverse('contact_user', kwargs={'user_id': settings.PHRF_DEFAULT_OFFICER_ID})
        self.assertContains(self.client.get(url), 'Contact Ada Chair')
