import json
import uuid
import random as r
from django.contrib import admin
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from base.admin import proposalAdmin
from base.models import user, ride, proposal


def getgeo(request):
    if request.user.is_authenticated:
        try:
            getlocation = ride.objects.get(username=request.user)
            getlocation.latitude = request.COOKIES.get('latitude')
            getlocation.longitude = request.COOKIES.get('longitude')
            getlocation.save()

        except:
            pass
    return HttpResponse('worked')


# this is the home page where you can see the list of available dispatch rider
def index(request):
    # dd = proposalAdmin(proposal)
    # dd.exclude = ['deliveryPassword']
    # admin.site.register(proposal)
    if request.method == 'GET':
        search = request.GET.get('search')

        # | Q(price__range=(0, search))
        if search:
            rides = ride.objects.filter(Q(verified=True) &
                                        (Q(rideName__icontains=search) | Q(state__icontains=search) | Q(
                                            rideDescription__icontains=search) | Q(
                                            rideType__icontains=search))).order_by('?')
            search = search
            p = Paginator(rides, 20)
            page = request.GET.get('page')
            page_pagination = p.get_page(page)

        else:

            rides = ride.objects.filter(verified=True).order_by('?')
            p = Paginator(rides, 20)
            page = request.GET.get('page')
            page_pagination = p.get_page(page)

    try:

        proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

        proposalr = proposal.objects.filter(Q(riderUsername=request.user.phoneNumber) & Q(accepted=False)).count

        goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                           & Q(accepted=True)).count
        goodstosend = proposal.objects.filter(
            Q(riderUsername=request.user.phoneNumber) & Q(accepted=True) & Q(deliver=False)).count
        goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user.phoneNumber)
                                               & Q(deliver=True)).count
    except:
        proposalr = '0'
        proposals = '0'
        goodsent = '0'
        goodsdeliver = '0'
        goodstosend = '0'

    context = {'rides': page_pagination, 'proposalr': proposalr, 'goodstosend': goodstosend,
               'goodsent': goodsent,
               'proposals': proposals, 'search': search, 'goodsdeliver': goodsdeliver
               }
    return render(request, 'base/index2.html', context)


@login_required(login_url='base:login')
# this method allow login users to send proposal to a dispatch rider
def sendproposal(request, pk):
    getrider = ride.objects.get(id=pk)
    getuser = user.objects.get(email=request.user.email)
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    if request.method == 'POST':
        goodsName = request.POST.get('goodsName')
        receiverName = request.POST.get('receiverName')
        receiverAddress = request.POST.get('receiverAddress')
        receiverNumber = request.POST.get('receiverNumber')
        goodsDescription = request.POST.get('goodsDescription')
        amount = request.POST.get('amount')

        code = ''
        for i in range(10):
            code += str(r.randint(1, 9))

        delivarypin = code

        propose = proposal(riderUsername=getrider.username, rideName=getrider.rideName,
                           riderPhoneNumber=getrider.phoneNumber, senderEmail=getuser.email,
                           senderPhoneNumber=getuser.phoneNumber, rideTrackId=getrider.id,
                           rideType=getrider.rideType, goodsName=goodsName, receiverPhoneNumber=receiverNumber,
                           receiverName=receiverName, receiverAddress=receiverAddress, amount=amount,
                           goodsDescription=goodsDescription, deliveryPassword=delivarypin,
                           senderName=getuser.fullName)
        messages.success(request, 'Proposal sent to dispatch Rider')

        propose.save()
        return redirect('base:proposalSent')

    context = {'getrider': getrider, 'getuser': getuser, 'proposalr': proposalr, 'goodstosend': goodstosend,
               'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    return render(request, 'base/sendProposal.html', context)


@login_required(login_url='base:login')
# this method allow login user to edit proposal he or she has saint
def proposalDetailsUpdate(request, pk):
    getproposal = proposal.objects.get(id=pk)
    if request.user.phoneNumber == getproposal.senderPhoneNumber:
        pass
    else:
        return redirect('base:index')
    messages.info(request, 'note: you can edit all this information here in this page')
    goodsName = request.POST.get('goodsName')
    receiverName = request.POST.get('receiverName')
    receiverAddress = request.POST.get('receiverAddress')
    receiverNumber = request.POST.get('receiverNumber')
    goodsDescription = request.POST.get('goodsDescription')
    amount = request.POST.get('amount')
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderName=request.user) & Q(accepted=True)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    if request.method == "POST":
        getproposal.goodsName = goodsName
        getproposal.receiverAddress = receiverAddress
        getproposal.receiverName = receiverName
        getproposal.receiverPhoneNumber = receiverNumber
        getproposal.goodsDescription = goodsDescription
        getproposal.amount = amount
        messages.success(request, 'Proposal Updated Successfully')
        getproposal.save()
        return redirect('base:proposalupdate', getproposal.id)
    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}

    return render(request, 'base/proposalSentDetail.html', context)


# this method make register user to login
def logins(request):
    if request.user.is_authenticated:
        return redirect('base:index')
    goodstosend = "0"
    proposals = "0"
    proposalr = '0'
    goodsent = '0'
    goodsdeliver = '0'
    number = request.POST.get('number')
    print(number)
    passwords = request.POST.get('password')
    if request.method == 'GET':
        cache.set('next', request.GET.get('next', None))
    if request.method == 'POST':
        getuser = authenticate(request, username=number.replace('+234', '0'), password=passwords)
        if getuser:
            next_url = cache.get('next')
            login(request, getuser)
            if next_url:
                cache.delete('next')
                return redirect(next_url)
            else:
                return redirect('base:index')

        else:
            messages.error(request, 'user credentials is not  correct')
    context = {'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}

    return render(request, 'base/login.html', context)


@login_required(login_url='base:login')
# this method shows the list of proposals login  users as received so far
def proposalReceive(request):
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    getproposal = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).order_by('-update')

    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    return render(request, 'base/proposalReceive.html', context)


@login_required(login_url='base:login')
# just to display the list of proposal login user has sent
def proposalSent(request):
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user) & Q(deliver=True)).count
    sentproposal = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).order_by(
        '-update')
    context = {'sentproposal': sentproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'goodsdeliver': goodsdeliver, 'proposals': proposals}
    return render(request, 'base/proposalSent.html', context)


@login_required(login_url='base:login')
# this method allow the Dispatch rider the freedom to accept proposal that is being sent to him
def acceptproposal(request, pk):
    getproposal = proposal.objects.get(id=pk)
    if request.user.phoneNumber == getproposal.riderUsername:
        pass
    else:
        return redirect('base:index')
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count

    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    if request.method == 'POST':

        text = 'Dear ' + getproposal.receiverName + ', you have a package from ' + getproposal.senderName + '\n your package will ' \
                                                                                                            'be ' \
                                                                                                            'deliver to you  soon \nRider Number: ' + str(
            getproposal.riderPhoneNumber) + '\n Delivery Pin is: ' + getproposal.deliveryPassword + ' \n give the delivery ' \
                                                                                                    'agent the  Delivery Pin after receiving the package '
        try:
            sendsms = requests.get(
                'https://portal.nigeriabulksms.com/api/?username=speedoo24434@gmail.com&password=adedejiboy1st.&message=' + text + '&sender=GDRider&mobiles=' + str(
                    getproposal.receiverPhoneNumber)).json()
            print(sendsms)
        except:
            messages.error(request, 'error occur please try again later ')
            return redirect('base:acceptProposal', getproposal.id)
        if 'status' in sendsms:
            getproposal.accepted = True
            getproposal.save()
            messages.success(request, 'Congratulation you have a new package to deliver')
            return redirect('base:onDelivary')
        else:
            messages.error(request, 'error occur please try again later ')
            return redirect('base:acceptProposal', getproposal.id)

        # return redirect('base:proposal-receive')
    return render(request, 'base/proposalReceivedDetail.html', context)


@login_required(login_url='base:login')
# this method shows the list of goods to deliver
def goodstoDeliver(request):
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count

    getproposal = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).order_by(
        '-update')
    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    return render(request, 'base/goodstoDeliver.html', context)


@login_required(login_url='base:login')
def goodSent(request):
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count

    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    getproposal = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=True)).order_by(
        '-update')
    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    return render(request, 'base/goodSent.html', context)


def signup(request):
    full_name = request.POST.get('full-name')
    email = request.POST.get('email')
    number = request.POST.get('number'.replace('+234', '0'))
    nin = request.FILES.get('nin')
    gender = request.POST.get('gender')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if request.method == 'POST':

        try:
            check = user.objects.get(phoneNumber=number.replace('+234', '0'))
        except:
            if password == confirm_password:
                request.session['email'] = email
                request.session['full_name'] = full_name
                request.session['number'] = number.replace('+234', '0')
                request.session['gender'] = gender
                # request.session['nin'] = nin
                request.session['password'] = password
                code = ''
                for i in range(6):
                    code += str(r.randint(1, 9))
                print(code)
                text = 'DO NOT DISCLOSE. Dear Customer The code for your Phone number authentication is ' + code + '., kindly make sure no one is watching you.'

                try:
                    sendsms = requests.get(
                        'https://portal.nigeriabulksms.com/api/?username=azeezadedeji638@gmail.com&password=adedejiboy1st.&message=' + text + '&sender=GDRider&mobiles=' + number).json()
                    print(sendsms)
                except:
                    messages.error(request, 'error getting otp code ')
                    return 'error'
                request.session['otp'] = make_password(code)
                messages.success(request, 'Verify your Account')
                return redirect('base:verify-account')
            else:
                messages.error(request, 'Password doesnt match ')
                return redirect("base:signup")
        messages.error(request, 'Account Already Exit')

    return render(request, 'base/signup.html')


def verfyaccount(request):
    # print(code)

    email = request.session.get('email')
    full_name = request.session.get('full_name')
    number = request.session.get('number')
    nin = request.session.get('nin')
    password = request.session.get('password')
    gender = request.session.get('gender')

    # if number == '':
    #     return redirect('base:signup')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        otps = check_password(otp, request.session.get('otp'))

        if otps == True:
            passwords = make_password(password)

            check = user(email=email, fullName=full_name, ninslip=nin, phoneNumber=number, password=passwords)
            check.save()
            request.session['email'] = ''
            request.session['full_name'] = ''
            request.session['number'] = ''
            request.session['gender'] = ''
            # request.session['nin'] = nin
            request.session['password'] = ''
            request.session['otp'] = ''
            messages.success(request, 'Account created successfully, you can now login.')

            return redirect('base:login')
        else:
            # request.session['email'] = ''
            # request.session['full_name'] = ''
            # request.session['number'] = ''
            # request.session['gender'] = ''
            # request.session['nin'] = nin
            # request.session['password'] = ''
            # request.session['otp'] = ''
            messages.error(request, 'otp code is incorrect')
            return redirect('base:verify-account')
    return render(request, 'base/accountVerification.html')


@login_required(login_url='base:login')
def createRide(request):
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    rideName = request.POST.get('rideName')
    rideType = request.POST.get('rideType')
    number = request.POST.get('number')
    amount = request.POST.get('amount')
    rideImage = request.FILES.get('rideImage')
    preview1 = request.FILES.get('preview1')
    preview2 = request.FILES.get('preview2')
    preview3 = request.FILES.get('preview3')
    preview4 = request.FILES.get('preview4')
    preview5 = request.FILES.get('preview5')

    rideDescription = request.POST.get('rideDescription')
    state = request.POST.get('state')
    lga = request.POST.get('lga')

    if request.method == 'POST':
        newride = ride(username=request.user.phoneNumber, phoneNumber=number, rideName=rideName,
                       image=rideImage, preview1=preview1, preview2=preview2,
                       preview3=preview3, preview4=preview4, price=amount, localGov=lga, preview5=preview5,
                       rideDescription=rideDescription, state=state, rideType=rideType)
        if newride:
            messages.info(request, 'Your Ride is still under review')
            newride.save()
    context = {'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}

    return render(request, 'base/rideCreate.html', context)


def rideDetails(request, pk):
    goodstosend = "0"
    proposals = "0"
    proposalr = '0'
    goodsent = '0'
    goodsdeliver = '0'
    try:
        proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
        proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

        goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                           & Q(accepted=True)).count
        goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
        goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                               & Q(deliver=True)).count
    except:
        pass
    getride = ride.objects.get(id=pk)
    rides = ride.objects.filter(verified=True)
    if getride.verified:
        if request.user == getride.username:
            messages.success(request, 'Congratulations your ride has been verified successfully, ')

    else:
        if request.user == getride.username:
            messages.error(request,
                           'your ride is yet to be verified, we will let you know if it has been verified successfully')

    context = {'getride': getride, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver, 'rides': rides}
    return render(request, 'base/rideDetails.html', context)


def maplocation(request, pk):
    getride = ride.objects.get(id=pk)
    context = {'latitude': getride.latitude, 'longitude': getride.longitude}
    return HttpResponse(json.dumps(context),
                        content_type="application/json"
                        )


@login_required(login_url='base:login')
def myride(request):
    rides = ride.objects.filter(username=request.user)
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    context = {'rides': rides, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}

    return render(request, 'base/myride.html', context)


@login_required(login_url='base:login')
def goodstodeliverpreview(request, pk):
    getproposal = proposal.objects.get(id=pk)
    if request.user.phoneNumber == getproposal.riderUsername:
        pass
    else:
        return redirect('base:index')

    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count
    if request.method == 'POST':
        deliverypassword = request.POST.get('delivery-password')
        if deliverypassword == getproposal.deliveryPassword:
            text = 'Dear ' + getproposal.senderName + ', your package has ben sent successfully to ' + getproposal.receiverName + '\n Thank you for using GDRider, we would like to partner with you some other days.'

            try:
                sendsms = requests.get(
                    'https://portal.nigeriabulksms.com/api/?username=speedoo24434@gmail.com&password=adedejiboy1st.&message=' + text + '&sender=GDRider&mobiles=' + str(
                        getproposal.senderPhoneNumber)).json()
                print(sendsms)
            except:
                messages.error(request, 'error occur please try again later ')
                return redirect('base:acceptProposal', getproposal.id)
            if 'status' in sendsms:
                getproposal.deliver = True
                getproposal.save()
                messages.success(request, 'Goods Delivered successfully')

                return redirect('base:goodsDeliver')
            else:
                messages.error(request, 'error occur please try again later ')
                return redirect('base:goods-to-deliver', getproposal.id)


        else:
            messages.error(request, 'incorrect Delivery Password')

    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}

    return render(request, 'base/goodstoDeliverPreview.html', context)


@login_required(login_url='base:login')
# this method show the list of goods that has been delivered
def goodsDelivered(request):
    getproposal = proposal.objects.filter(Q(riderUsername=request.user.phoneNumber) & Q(deliver=True)).order_by(
        '-update')

    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(
        Q(riderUsername=request.user.phoneNumber) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user.phoneNumber)
                                           & Q(deliver=True)).count
    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    return render(request, 'base/goodsDelivered.html', context)


def loguserout(request):
    logout(request)
    return redirect('base:login')


def delivered(request, pk):
    proposalr = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=False)).count
    proposals = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber) & Q(accepted=False)).count

    goodsent = proposal.objects.filter(Q(senderPhoneNumber=request.user.phoneNumber)
                                       & Q(accepted=True)).count
    goodstosend = proposal.objects.filter(Q(riderUsername=request.user) & Q(accepted=True) & Q(deliver=False)).count
    goodsdeliver = proposal.objects.filter(Q(riderUsername=request.user)
                                           & Q(deliver=True)).count

    getproposal = proposal.objects.get(id=pk)
    if request.user.phoneNumber == getproposal.riderUsername or request.user.phoneNumber == getproposal.senderPhoneNumber:
        if getproposal.deliver:
            messages.success(request, 'This goods as been delivered successfully')
        else:
            messages.warning(request, 'This goods is yet to be delivered')
    else:
        return redirect('base:index')
    context = {'getproposal': getproposal, 'proposalr': proposalr, 'goodstosend': goodstosend, 'goodsent': goodsent,
               'proposals': proposals, 'goodsdeliver': goodsdeliver}
    return render(request, 'base/goodsDeliveredDetails.html', context)


def proposalDelete(request, pk):
    getproposal = proposal.objects.get(id=pk)
    getproposal.delete()
    messages.error(request, 'proposal has been deleted successfully')
    return redirect('base:proposalSent')


def profile(request):
    return render(request, 'base/profile.html')


def forgetPassword(request):
    if request.user.is_authenticated:
        return redirect('base:index')
    if request.method == 'POST':
        number = request.POST.get('number')
        try:
            user.objects.get(phoneNumber=number)
        except:
            messages.error(request, 'Number does not exit')
            return render(request, 'base/resetPassword.html')
        request.session['number'] = number.replace('+234', '0')
        code = ''
        for i in range(6):
            code += str(r.randint(1, 9))

        text = 'DO NOT DISCLOSE. Dear Customer The code for your Phone number authentication is ' + code + '., kindly make sure no one is watching you.'

        try:
            sendsms = requests.get(
                'https://portal.nigeriabulksms.com/api/?username=azeezadedeji638@gmail.com&password=adedejiboy1st.&message=' + text + '&sender=GDRider&mobiles=' + number).json()
            print(sendsms)
        except:
            messages.error(request, 'error getting otp code ')
            return 'error'
        request.session['otp'] = make_password(code)
        messages.success(request, 'Verify your Account')
        return redirect('base:reset-password-verify')
    return render(request, 'base/resetPassword.html')


def resetPasswordVerify(request):
    if request.user.is_authenticated:
        return redirect('base:index')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        ps = request.POST.get('password')
        passwords = make_password(ps)
        otps = check_password(otp, request.session.get('otp'))
        if otps:
            userid = user.objects.get(phoneNumber=request.session.get('number'))
            userid.password = passwords
            userid.save()
            messages.success(request, 'Password change successfully')
            request.session['number'] = ''
            request.session['otp'] = ''
            return redirect('base:login')
        else:
            messages.error(request, 'incorrect  otp code')

    return render(request, 'base/resetPasswordVerification.html')
