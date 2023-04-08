# Generated by Django 4.1.3 on 2023-03-25 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_ride_rideid_proposal_rideid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='rideId',
        ),
        migrations.AddField(
            model_name='proposal',
            name='rideName',
            field=models.CharField(default='empty', max_length=50),
        ),
        migrations.AddField(
            model_name='proposal',
            name='riderUsername',
            field=models.CharField(default='null', max_length=50),
        ),
    ]
