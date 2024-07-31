from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    if "watchlist_count" not in request.session:
        request.session["watchlist_count"] = 0

    listings = Listing.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": listings,
        "categories": categories
    })


def index_category(request):
    if request.method == "POST":
        categories = Category.objects.get(name=request.POST["category"])
        listings = Listing.objects.filter(is_active=True, category=categories)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": listings,
            "categories": categories
        })


def add_watchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        user = request.user
        listing.watchlist.add(user)
        request.session["watchlist_count"] += 1
        return HttpResponseRedirect(reverse("listing", args=(id, )))


def delete_watchlist(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        user = request.user
        listing.watchlist.remove(user)
        request.session["watchlist_count"] -= 1
        return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist(request):
    user = request.user
    user_watchlists = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": user_watchlists
    })


def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image_url = request.POST["image_url"]

        user = request.user
        category = Category.objects.get(name=request.POST["category"])
        bid = Bid(
            bid = float(price),
            user = user
        )
        bid.save()

        new_listing = Listing(
            title = title,
            description = description,
            price = bid,
            image_url = image_url,
            owner = user,
            category = category
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))


def listing(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    is_in_watchlist = user in listing.watchlist.all()
    comments = listing.listing_comment.all()

    can_close_listing = False
    owner = listing.owner
    if user.username == owner.username:
        can_close_listing = True

    bit_congratulation = False
    if listing.is_active == False and user.username == listing.price.user.username:
        bit_congratulation = True

    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "is_in_watchlist": is_in_watchlist,
        "comments": comments,
        "can_close_listing": can_close_listing,
        "bit_congratulation": bit_congratulation
    })


def listing_close(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))


def comment(request, id):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        listing = Listing.objects.get(pk=id)

        new_comment = Comment(
            content = content, 
            author = user,
            listing = listing
        )
        new_comment.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))


def bid(request, id):
    if request.method == "POST":
        bid = float(request.POST["bid"])
        listing = Listing.objects.get(pk=id)
        comments = listing.listing_comment.all()
        if listing.price.bid < bid:
            update_bit = Bid(
                bid = bid,
                user = request.user
            )
            update_bit.save()
            listing.price = update_bit
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing, 
                "message": "Bid updated successfully",
                "comments": comments,
                "updated": True
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing, 
                "message": "Bid failed",
                "comments": comments,
                "updated": False
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
        return render(request, "auctions/login.html")


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

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
