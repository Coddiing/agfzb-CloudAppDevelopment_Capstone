from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def simple_django_view( request ):
    return render( request, 'djangoapp/static_page.html' )


# Create an `about` view to render a static about page
def about( request ):
    return render( request, 'djangoapp/about.html' )

# Create a `contact` view to return a static contact page
def contact(request):
    return render( request, 'djangoapp/contact.html' )

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method=='POST':
        user = request.POST[ 'username' ]
        password = request.POST[ 'psw' ]

        user = authenticate( username=user, password=password )

        if user is not None:
            login( request, user )
        
        return redirect( 'djangoapp:index' )
       

    return HttpResponseRedirect( reversed( 'index' ) )


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print ( 'Logging you out' )
    logout( request )

    return redirect( 'djangoapp:index' )

def signup_view( request ):
    context = {
        'err': ''
    }
    return render( request, 'djangoapp/registration.html', context ) 

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        user_exist = False
        username = request.POST[ 'username' ]
        email = request.POST[ 'email' ]
        f_name = request.POST[ 'f_name' ]
        l_name = request.POST[ 'l_name' ]
        psw = request.POST[ 'psw' ]
        psw2 = request.POST[ 'psw2' ]


        if psw != psw2:
            return render( request, 'djangoapp/registration.html', {
                'err': 'Error! Passwords do not match... {0}, {1}'.format( psw, psw2 )
            } )  
        try:
            User.objects.get(username=username)
            user_exist = True
            
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user( username, email, psw, first_name=f_name, last_name=l_name )
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', 
            {
                'err': 'You are already in our database'
            })

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":

        url = "https://6c01f567.us-south.apigw.appdomain.cloud/api/dealerships/api/dealerships"

        dealerships = get_dealers_from_cf( url )

        dealer_names = ''.join( [dealer.short_name for dealer in dealerships] )


        return HttpResponse( dealer_names )
        #return render(request, 'djangoapp/index.html', context)

    


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}

    if request.method=="GET":

        url = "https://6c01f567.us-south.apigw.appdomain.cloud/review/api/review"

        reviews = get_dealer_reviews_from_cf ( url, dealer_id )

        review_names = '; '.join( [rev.review for rev in reviews] )


        return HttpResponse( review_names )


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

