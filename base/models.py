import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class user(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True)
    fullName = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=20, unique=True)
    localGoverment = models.CharField(max_length=2000, null=True, blank=True)
    state = models.CharField(max_length=1000, blank=True, null=True)
    wallet = models.TextField(default='0')
    fund_wallet = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    verify = models.BooleanField(default=False)
    USERNAME_FIELD = 'phoneNumber'


class ride(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    username = models.CharField(max_length=50)
    rideName = models.CharField(max_length=100)
    rideType = models.CharField(max_length=50)

    phoneNumber = models.CharField(max_length=20)
    image = models.ImageField()
    preview1 = models.ImageField()
    preview2 = models.ImageField()
    preview3 = models.ImageField()
    preview4 = models.ImageField()
    preview5 = models.ImageField()

    rideDescription = models.TextField()
    latitude = models.CharField(max_length=100, default='null')
    longitude = models.CharField(max_length=100, default='null')
    state = models.CharField(max_length=100)
    localGov = models.CharField(max_length=200)
    price = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    verified = models.BooleanField(default=False)


class proposal(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    riderUsername = models.CharField(max_length=50, default='null')

    rideName = models.CharField(max_length=50, default='empty')
    riderEmail = models.EmailField()
    senderName = models.CharField(max_length=100, default='empty')
    riderPhoneNumber = models.CharField(max_length=20, default='empty')
    senderEmail = models.EmailField()
    senderPhoneNumber = models.CharField(max_length=20, default='empty')
    rideTrackId = models.CharField(max_length=100)
    rideType = models.CharField(max_length=50)
    goodsName = models.CharField(max_length=250)
    receiverName = models.CharField(max_length=250)
    receiverAddress = models.CharField(max_length=250)
    receiverPhoneNumber = models.CharField(max_length=50)
    amount = models.TextField()
    formerAmount = models.TextField(blank=True, null=True)
    goodsDescription = models.TextField()
    deliveryPassword = models.CharField(max_length=10, blank='True', null='True')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    deliver = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.goodsName[:10] + ' : ' + str(self.id)
