from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Ad, AppliedBy

# Create your views here.
def index(request):
    is_influencer = False
    is_advertiser = False
    print(request.user.is_advertiser)
    if request.user.is_influencer:
        is_influencer = True

    if request.user.is_advertiser:
        is_advertiser = True

    
    appl = AppliedBy.objects.filter(influencer=request.user)
    # ads_applied = Ad.objects.filter( id = AppliedBy.objects.filter(influencer=request.user).values_list('id', flat=True))
    # ads_not_applied = Ad.objects.exclude(pk__in=ads_applied.values_list('ad', flat=True))
    ads_applied = Ad.objects.filter(id__in=AppliedBy.objects.filter(influencer=request.user).values_list('ad', flat=True))
    ads_not_applied = Ad.objects.exclude(id__in=AppliedBy.objects.filter(influencer=request.user).values_list('ad', flat=True))
    return render(request, 'ads/index.html', {
        "is_influencer": is_influencer,
        "is_advertiser": is_advertiser,
        "ads_accepted_by_user": ads_applied,
        "ads_not_accepted_by_user": ads_not_applied
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ads/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        print(request.POST)
        
        try :
            if request.POST["is_influencer"]:
                is_influencer = True
        except :
            is_influencer = False

        try :
            if request.POST["is_advertiser"]:
                is_advertiser = True
        except :
            is_advertiser = False
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, is_influencer=is_influencer, is_advertiser=is_advertiser)
            user.save()
        except IntegrityError:
            return render(request, "ads/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ads/register.html")
    

def create_ad(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        try:
            image = request.POST["image"]
        except:
            image = None

        price = int(price)
        author = request.user
        ad = Ad(title=title, description=description, price=price, image=image, author=author)
        ad.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ads/create_ad.html")
    
def ad(request, ad_id):
    ad = Ad.objects.get(pk=ad_id)
    is_advertiser = False
    if request.user.is_advertiser:
        is_advertiser = True
    is_influencer = False
    if request.user.is_influencer:
        is_influencer = True
    did_apply = False
    if AppliedBy.objects.filter(ad=ad, influencer=request.user):
        did_apply = True
    return render(request, "ads/display_ad.html", {
        "ad": ad,
        "is_advertiser": is_advertiser,
        "is_influencer": is_influencer,
        "did_apply": did_apply
    })

def apply(request, ad_id):
    ad = Ad.objects.get(pk=ad_id)
    influencer = request.user
    # check if already applied
    appliedby = AppliedBy.objects.filter(ad=ad, influencer=influencer)
    if appliedby:
        return HttpResponseRedirect(reverse("index"))
    appliedby = AppliedBy(ad=ad, influencer=influencer, accepted=True, rejected=False)
    appliedby.save()
    return HttpResponseRedirect(reverse("index"))