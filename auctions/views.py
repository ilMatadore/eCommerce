from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max

from .models import User, Product, Category, Watchlist, Comment, Bid

from django.forms import ModelForm, Textarea, Select, TextInput, NumberInput


class Create(ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'category',
                  'starting_bid', 'image')
        widgets = {'category': Select(choices=Category.objects.all(), attrs={'class': 'form-control'}),
                   'title': TextInput(attrs={'class': 'form-control'}),
                   'description': Textarea(attrs={'class': 'form-control'}),
                   'starting_bid': NumberInput(attrs={'class': 'form-control'})
                   }


def index(request):
    return render(request, "auctions/index.html", {
        "products": Product.objects.all()
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


def create(request):
    user = request.user
    if request.method == 'POST':
        form = Create(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']
            starting_bid = form.cleaned_data['starting_bid']

            Product.objects.create(
                user=user,
                title=title,
                description=description,
                category=category,
                image=image,
                starting_bid=starting_bid
            )

            return redirect('index')

    else:
        return render(request, "auctions/create.html", {
            "form": Create()
        })


def product(request, product_id):
    message = ''
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(
        product=product_id).order_by('date_created').reverse
    bids = Bid.objects.filter(product=product)
    maxBid = Bid.objects.filter(product=product).aggregate(Max('bid'))
    # if Bid.objects.order_by('bid') is None:
    #     maxBidUser = ''
    # else:
    maxBidUser = Bid.objects.order_by('bid').last().user
    # Bid.objects.latest('bid').user

    if request.method == "POST":

        if 'auction_status' in request.POST:
            product.closed = request.POST['auction_status']
            product.save()
        elif 'comment' in request.POST:
            toComment = Comment.objects.filter(product=product_id)
            newComment = Comment.objects.create(
                comment=request.POST['comment'], user=request.user, product=product)
            newComment.save()
        elif 'bid' in request.POST:
            if maxBid['bid__max'] == None:
                if int(request.POST['bid']) < product.starting_bid:
                    message = "Bid must be higher than starting bid"

                else:
                    message = "Your bid has been placed!"
                    watchlist = Watchlist.objects.get(user=request.user)
                    watchlist.product.add(product)
                    newBid = Bid.objects.create(
                        bid=int(request.POST['bid']), user=request.user, product=product)

                    product.lastBid = int(request.POST['bid'])
                    product.save()
                    maxBid = Bid.objects.filter(
                        product=product).aggregate(Max('bid'))
                    # current_URL = request.META.get('HTTP_REFERER')
                    # return redirect(current_URL)
            else:
                if int(request.POST['bid']) <= maxBid['bid__max']:
                    message = "Bid must be higher than current bid"

                else:
                    message = "Your bid has been placed!"
                    watchlist = Watchlist.objects.get(user=request.user)
                    watchlist.product.add(product)
                    newBid = Bid.objects.create(
                        bid=int(request.POST['bid']), user=request.user, product=product)
                    print(message)
                    product.lastBid = int(request.POST['bid'])
                    product.save()
                    maxBid = Bid.objects.filter(
                        product=product).aggregate(Max('bid'))
                    # current_URL = request.META.get('HTTP_REFERER')
                    # return redirect(current_URL)

    if request.user.is_authenticated:

        watchlist = Watchlist.objects.get(user=request.user)
        return render(request, "auctions/product.html", {
            "product": product,
            "watchlist": watchlist,
            "comments": comments,
            "message": message,
            "bids": bids,
            "maxBid": maxBid,
            "maxBidUser": maxBidUser

        })
    else:

        return render(request, "auctions/product.html", {
            "product": product,
            "comments": comments,
            "message": message,
            "bids": bids,
            "maxBid": maxBid,
            "maxBidUser": maxBidUser

        })


def watchlist(request):
    products = Watchlist.objects.get(user=request.user)
    totalProducts = products.product.count()
    return render(request, "auctions/watchlist.html", {
        "products": products,
        'totalProducts': totalProducts,

    })


def remove_watchlist(request, product_id):
    product = Product.objects.get(id=product_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.product.remove(product)
    watchlist.save()
    current_URL = request.META.get('HTTP_REFERER')
    return redirect(current_URL)


def add_watchlist(request, product_id):
    product = Product.objects.get(id=product_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.product.add(product)
    watchlist.save()
    current_URL = request.META.get('HTTP_REFERER')
    return redirect(current_URL)


def categories(request):

    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def sort_by_category(request, category_id):
    return render(request, "auctions/index.html", {
        "products": Product.objects.all().filter(category=category_id)
    })
