# Generated by Django 4.1.3 on 2023-03-31 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_proposal_sendername'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='latitude',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='ride',
            name='longitude',
            field=models.CharField(default='null', max_length=100),
        ),
    ]
