# Generated by Django 2.1.8 on 2019-06-04 18:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boat_name', models.CharField(max_length=255)),
                ('boat_type', models.CharField(max_length=255)),
                ('sail_number', models.CharField(max_length=25)),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2019)])),
                ('length_overall', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('waterline_length', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('beam', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('draft', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('displacement', models.PositiveIntegerField(blank=True, null=True)),
                ('ballast', models.PositiveIntegerField(blank=True, null=True)),
                ('keel', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Centerboard'), (2, 'Daggerboard'), (3, 'Fin'), (4, 'Full'), (5, 'Shoal'), (6, 'Swing'), (7, 'Wing')], null=True)),
                ('prop', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Folding / feathering'), (2, 'Solid 2-blade in an aperture'), (3, 'Outboard retracted when racing'), (4, 'Solid 2-blade out of an aperture'), (5, 'Outboard not retracted when racing'), (6, 'Solid 3-blade in an aperture'), (7, 'Solid 3-blade out of an aperture')], null=True)),
                ('max_headsail', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Up to 125.0'), (2, '125.1-135.0'), (3, '135.1-145.0'), (4, '145.1-155.0'), (5, '155.1-165.0'), (6, '165.1-175.0'), (7, '175.1-185.0'), (8, '185.1-195.0'), (9, '195.1 and over')], null=True)),
                ('i', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('j', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('p', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('e', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('rig_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Fractional'), (2, 'Masthead')], null=True)),
                ('mast_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Standard'), (2, 'Tall')], null=True)),
                ('spin_type', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Asymmetrical'), (2, 'Symmetrical'), (3, 'Both'), (4, 'None')], null=True)),
                ('spin_pole_length', models.DecimalField(blank=True, decimal_places=2, help_text='Enter spin pole length if different than standard.', max_digits=5, null=True)),
                ('spin_luff', models.DecimalField(blank=True, decimal_places=2, help_text='Enter spin luff length if different than standard', max_digits=5, null=True)),
                ('spin_max_girth', models.DecimalField(blank=True, decimal_places=2, help_text='Enter spin max girth length if different than standard', max_digits=5, null=True)),
                ('modifications', models.TextField(blank=True, help_text='Describe any non-standard modifications to the vessels hull or rig.', null=True)),
            ],
            options={
                'ordering': ['boat_name', 'boat_type'],
            },
        ),
        migrations.CreateModel(
            name='Cert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_rating', models.IntegerField()),
                ('adjusted_rating', models.IntegerField()),
                ('non_spin_rating', models.IntegerField(blank=True, null=True)),
                ('expiration_date', models.DateField()),
                ('updated', models.DateField(auto_now=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('application_date', models.DateField()),
                ('boat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='phrf.Boat')),
            ],
            options={
                'ordering': ['-expiration_date', 'boat__boat_name', 'boat__owner__last_name'],
            },
        ),
        migrations.CreateModel(
            name='CertRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')])),
                ('application_date', models.DateField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'new'), (2, 'pending'), (3, 'complete')], default=1)),
                ('comments', models.TextField(blank=True, null=True)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phrf.Boat')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('club', models.PositiveSmallIntegerField(choices=[(0, 'None'), (1, 'BFSC'), (2, 'LLSC'), (3, 'SSC'), (4, 'UYC')], default=0)),
                ('mailing_list', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['user__last_name', 'user__first_name'],
            },
        ),
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(blank=True, null=True)),
                ('request_date', models.DateField(auto_now_add=True)),
                ('boat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phrf.Boat')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='certrequest',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='boat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='boat',
            unique_together={('owner', 'boat_name', 'boat_type', 'sail_number')},
        ),
    ]