from django.urls import path

from base import views

app_name = 'base'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.logins, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create-ride/', views.createRide, name='ride'),
    path('rider-details/<str:pk>/', views.rideDetails, name='rideDetails'),
    path('send-proposal/<str:pk>/', views.sendproposal, name='sendproposal'),
    path('proposal-receive/', views.proposalReceive, name='proposal-receive'),
    path('proposal-sent/', views.proposalSent, name='proposalSent'),
    path('accept-proposal/<str:pk>/', views.acceptproposal, name='acceptProposal'),

    path('proposal-update/<str:pk>/', views.proposalDetailsUpdate, name='proposalupdate'),
    path('goods-to-deliver/', views.goodstoDeliver, name='onDelivary'),
    path('goods-sent', views.goodSent, name='goodSent'),
    path('log-out', views.loguserout, name='logout'),
    path('get-geo', views.getgeo, name='getgeo'),

    path('maplocation/<str:pk>/', views.maplocation, name='maplocation'),
    path('goods-to-deliver/<str:pk>', views.goodstodeliverpreview, name='goods-to-deliver'),

    path('my-ride-list', views.myride, name='myride'),
    path('goods-Delivered', views.goodsDelivered, name='goodsDeliver'),

    path('my-ride', views.myride, name='my-ride'),
    path('Delivered/<str:pk>', views.delivered, name='delivered'),
    path('proposal-delete/<str:pk>', views.proposalDelete, name='proposal-delete'),
    path('verify-account/', views.verfyaccount, name='verify-account'),
    path('profile', views.profile, name='profile')
]
