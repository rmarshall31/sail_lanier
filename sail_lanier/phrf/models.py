from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ProfileManagerOfficer(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            user__groups__name__in=["Club Representative", "Chairman", "Member at Large", "Measurer",
                                    "Secretary/Treasurer"])


class Profile(models.Model):
    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    club_choices = (
        (0, "None"),
        (1, "BFSC"),
        (2, "LLSC"),
        (3, "SSC"),
        (4, "UYC"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    club = models.PositiveSmallIntegerField(choices=club_choices, default=0)
    mailing_list = models.BooleanField(default=True)

    objects = models.Manager()
    officers = ProfileManagerOfficer()

    @property
    def name(self):
        return "{first_name} {last_name}".format(first_name=self.user.first_name, last_name=self.user.last_name)

    @property
    def group(self):
        return self.user.groups.first()

    @property
    def email(self):
        return self.user.email


class Boat(models.Model):
    class Meta:
        ordering = ["boat_name", "boat_type"]
        unique_together = ("owner", "boat_name", "boat_type", "sail_number")

    def __str__(self):
        return ("{boat_name} - {boat_type} - {owner_name}".format(boat_name=self.boat_name, boat_type=self.boat_type,
                                                                  owner_name=self.owner.last_name))

    keel_choices = (
        (1, "Centerboard"),
        (2, "Daggerboard"),
        (3, "Fin"),
        (4, "Full"),
        (5, "Shoal"),
        (6, "Swing"),
        (7, "Wing"),
    )

    prop_choices = (
        (1, "Folding / feathering"),
        (2, "Solid 2-blade in an aperture"),
        (3, "Outboard retracted when racing"),
        (4, "Solid 2-blade out of an aperture"),
        (5, "Outboard not retracted when racing"),
        (6, "Solid 3-blade in an aperture"),
        (7, "Solid 3-blade out of an aperture"),
    )

    rig_choices = (
        (1, "Fractional"),
        (2, "Masthead"),
    )

    mast_choices = (
        (1, "Standard"),
        (2, "Tall"),
    )

    headsail_choices = (
        (1, "Up to 125.0"),
        (2, "125.1-135.0"),
        (3, "135.1-145.0"),
        (4, "145.1-155.0"),
        (5, "155.1-165.0"),
        (6, "165.1-175.0"),
        (7, "175.1-185.0"),
        (8, "185.1-195.0"),
        (9, "195.1 and over"),
    )

    spin_choices = (
        (1, "Asymmetrical"),
        (2, "Symmetrical"),
        (3, "Both"),
        (4, "None"),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    boat_name = models.CharField(max_length=255)
    boat_type = models.CharField(max_length=255)
    sail_number = models.CharField(max_length=25)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(date.today().year)], blank=True, null=True)
    length_overall = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    waterline_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    beam = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    draft = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    displacement = models.PositiveIntegerField(blank=True, null=True)
    ballast = models.PositiveIntegerField(blank=True, null=True)
    keel = models.PositiveSmallIntegerField(choices=keel_choices, blank=True, null=True)
    prop = models.PositiveSmallIntegerField(choices=prop_choices, blank=True, null=True)
    max_headsail = models.PositiveSmallIntegerField(choices=headsail_choices, blank=True, null=True)
    i = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    j = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    p = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    e = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    rig_type = models.PositiveSmallIntegerField(choices=rig_choices, blank=True, null=True)
    mast_type = models.PositiveSmallIntegerField(choices=mast_choices, blank=True, null=True)
    spin_type = models.PositiveSmallIntegerField(choices=spin_choices, blank=True, null=True)
    spin_pole_length = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                           help_text="Enter spin pole length if different than standard.")
    spin_luff = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                    help_text="Enter spin luff length if different than standard")
    spin_max_girth = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                         help_text="Enter spin max girth length if different than standard")

    modifications = models.TextField(blank=True, null=True,
                                     help_text="Describe any non-standard modifications to the vessels hull or rig.")

    @property
    def owner_name(self):
        return self.owner.last_name


class CertManagerValid(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(expiration_date__gte=date.today())


class Cert(models.Model):
    class Meta:
        ordering = ["-expiration_date", "boat__boat_name", "boat__owner__last_name"]

    def __str__(self):
        return ("{boat_name} - {owner_name} - {adjusted_rating}".format(boat_name=self.boat.boat_name,
                                                                        owner_name=self.boat.owner.last_name,
                                                                        adjusted_rating=self.adjusted_rating))

    boat = models.OneToOneField(Boat, on_delete=models.CASCADE)
    base_rating = models.IntegerField()
    adjusted_rating = models.IntegerField()
    non_spin_rating = models.IntegerField(blank=True, null=True)
    expiration_date = models.DateField(db_index=True)
    updated = models.DateField(auto_now=True)
    comments = models.TextField(blank=True, null=True)
    application_date = models.DateField()

    objects = models.Manager()
    valid = CertManagerValid()

    @property
    def boat_name(self):
        return self.boat.boat_name

    @property
    def boat_type(self):
        return self.boat.boat_type

    @property
    def owner_name(self):
        return self.boat.owner.last_name

    @property
    def sail_number(self):
        return self.boat.sail_number


class CertRequest(models.Model):
    year_choices = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
    )

    status_choices = (
        (1, "new"),
        (2, "pending"),
        (3, "complete"),
    )

    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    years = models.PositiveSmallIntegerField(choices=year_choices)
    application_date = models.DateField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=status_choices, default=1)
    comments = models.TextField(blank=True, null=True)


class TransferRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    request_date = models.DateField(auto_now_add=True)


# this forces the admin site to show the user's first and last name in drop downs instead of the username
def user_full_name(self):
    return self.get_full_name()


User.__str__ = user_full_name
