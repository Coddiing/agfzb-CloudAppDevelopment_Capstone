import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
from .api  import get_api

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    #try:
        # Call get method of requests library with URL and parameters
    api_key = get_api()
    print( "kwargs: "+str( kwargs ) )

    params = dict()
    if 'text' in kwargs:
        params[ 'text' ] = kwargs[ 'text' ]
        params[ 'version' ] = kwargs[ 'version' ]
        params[ 'feature' ] = kwargs[ 'feature' ]
        params[ 'return_analyzed_text' ] = kwargs[ 'return_analyzed_text' ]
        response = requests.get( url, headers={'Content-Type': 'application/json'},
                                params=params, auth=HTTPBasicAuth( 'apikey', api_key ) )
        print( "Response: {0}" .format( response ) )
    else:
        response = requests.get( url, headers={'Content-Type': 'application/json'},
                                params=kwargs, auth=HTTPBasicAuth( 'apikey', api_key ) )

    #except:
        # If any error occurs
    print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    print ( 'json_result: ' + str(json_result) )
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
         
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    #print ( 'kwargs: ' + str(json_result) ) 
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["reviews"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object

            purchase_date = ''
            car_make = ''
            car_model = ''
            car_year = ''
            if 'purchase_date' in dealer_doc:
                purchase_date = dealer_doc[ 'purchase_date' ]

            if 'car_year' in dealer_doc:
                car_year = dealer_doc[ 'car_year' ]

            if 'car_model' in dealer_doc:
                car_model = dealer_doc[ 'car_model' ]

            if 'car_make' in dealer_doc:
                car_make = dealer_doc[ 'car_make' ]


            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=dealer_doc["dealership"], name=dealer_doc["name"],
                                   purchase=dealer_doc["purchase"],
                                   review=dealer_doc["review"], purchase_date=purchase_date, car_make=car_make,
                                   car_model=car_model,
                                   car_year=car_year, sentiment='', id=dealer_doc["id"] )
            review_obj.sentiment = analyze_review_sentiments( review_obj.review )

            results.append(review_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    # - Call get_request() with specified arguments
    # - Get the returned sentiment label such as Positive or Negative

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/23c313df-d64d-4069-afe1-278753c9760d"
    json_result = get_request( url=url, text=dealerreview, version="1.1", feature='white', 
    return_analyzed_text="returned text" )

    #print( "json: {0}" .format( json_result ) )

    return json_result

    

    # response = requests.get( url, headers={'Content-Type': 'application/json'},
    #                                 params=params, auth=HTTPBasicAuth( 'apikey', get_api() ) )
    
    # status_code = response.status_code
    # print("With status {} ".format(status_code))
    # json_data = json.loads(response.text)
    # return json_data


def post_request( url, json_payload, **kwargs ):
    return requests.post( url, params=kwargs, json=json_payload )





