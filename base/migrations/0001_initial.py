# Generated by Django 4.1.3 on 2023-03-23 14:37

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fullName', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phoneNumber', models.CharField(max_length=20, unique=True)),
                ('ninslip', models.ImageField(upload_to='')),
                ('verify', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='proposal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('riderEmail', models.EmailField(max_length=254)),
                ('riderPhoneNumber', models.IntegerField()),
                ('senderEmail', models.EmailField(max_length=254)),
                ('senderPhoneNumber', models.IntegerField()),
                ('rideTrackId', models.CharField(max_length=100)),
                ('rideType', models.CharField(max_length=50)),
                ('goodsName', models.CharField(max_length=250)),
                ('receiverName', models.CharField(max_length=250)),
                ('receiverAddress', models.CharField(max_length=250)),
                ('receiverPhoneNumber', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('goodsDescription', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('deliver', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ride',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rideId', models.CharField(max_length=500)),
                ('rideName', models.CharField(max_length=100)),
                ('rideType', models.CharField(max_length=50)),
                ('ridePlateNumber', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='')),
                ('preview1', models.ImageField(upload_to='')),
                ('preview2', models.ImageField(upload_to='')),
                ('preview3', models.ImageField(upload_to='')),
                ('preview4', models.ImageField(upload_to='')),
                ('preview5', models.ImageField(upload_to='')),
                ('ridePlateNumberImage', models.ImageField(upload_to='')),
                ('rideDescription', models.TextField()),
                ('state', models.CharField(max_length=100)),
                ('localGov', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=1000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
