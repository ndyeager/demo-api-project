import tweepy
import lob
import googlemaps
import sunlight

# imports for Weather API
import urllib2
import json

from datetime import datetime

lob.api_key = "test_32f9cf853c605d272e35567fadb984b4318"
gmaps = googlemaps.Client(key='AIzaSyBuBYoY9OiVXnJnQf3D1jFG_iBOjqJkzw8')
sunlight.config.API_KEY = "ed9d8054bcca4773a803aa8c9b77e79a"
# Tweepy Setup
auth = tweepy.OAuthHandler('09mB3DUJsg9agik4sGw4DJ0jA', 'wM4focfIFuE8Gz3f2EX3dM3EHox4BVRNbedjNdchM24vRlRObL')
auth.set_access_token('1559211414-3ApuTjxIy7Ivr25Vn6GXHUNSEjYa8SE9H6yCbLR', 'FosDpZ9S0pSU0omTfnbpCG8rF14S85VRVJ1wb2ngdNhgc')
api = tweepy.API(auth)
# Weather API setup


def getAddressWithZip():
    # Testing for accurate zip code
    while True:
        try:
            zipCode = input("Please enter your five-digit zip code: ")
            if len(str(zipCode)) == 5:
                addressLine1, addressLine2 = getAddressLines()
                break
            else:
                print("The zip code entered is not five digits.")
        except (NameError, SyntaxError):
            print("The zip code entered was invalid.")

    city = ""
    state = ""
    return addressLine1, addressLine2, city, state, zipCode

def getAddressLines():

    # Requesting user's address line 1 and verifying that the string entered is not empty
    while True: 
        addressLine1 = raw_input("Please enter the first line of your address: ")
        if len(addressLine1.strip()) == 0:
            print("Try again, please.")
        else:
            break
            
    # Requesting user's address line 2 and ensuring that the user enters second address line if necessary. If         
    # the user does not have a second address line, the user will have to note this with line2response.
    while True:
        addressLine2 = raw_input("Please enter the second line of your address: ")
        if len(addressLine2.strip()) == 0:
            line2response = raw_input("Are you sure? ")
            if line2response == "yes" or line2response == "y":
                break
        else:
            break

    return addressLine1, addressLine2

def getAddressNoZip(): 
    # Retrieving address line 1
    print "Please enter your full address. *For cities that use a quadrant system, be sure to include your quadrant as a part of your street address. Otherwise, your address will be invalid!"
    addressLine1, addressLine2 = getAddressLines()
    while True: 
        city = raw_input("Please enter your City: ")
        if city.isspace() == True or city.replace(" ", "").isalpha() == False:
               print("Try again, please.")
        else:
               break             

    states = lob.State.list()

    stateFound = False
    
    print("Enter AA, AE, or AP for Armed Forces abroad")
    print("Enter VI or Virgin Islands for the US Virgin Islands")

    while stateFound == False:
        state = raw_input("Please enter your State: ")
        for x in states["data"]:
            if state.upper() in x.values() or state.title() in x.values():
                stateFound = True
                break       
    
    zipCode = ""
    
    return addressLine1, addressLine2, city, state, zipCode    
        


#checks if user knows Zip
zipVerify = raw_input("Do you know your zip code? ").lower()
# if User knows zip, the user is asked for the rest of their address 
# through the getAddressWithZip function
if zipVerify == "yes" or zipVerify == "y":
    addressLine1, addressLine2, city, state, zipCode = getAddressWithZip()
#if user doesn't know their zip code, the user is asked for city and state 
# through the getAddressNoZip function
elif zipVerify == "no" or zipVerify == "n":
    addressLine1, addressLine2, city, state, zipCode = getAddressNoZip()
else:
    print("You have entered an invalid response. ")
# this runs if user enters something other than "yes" or "no" 

verifiedAddress = lob.Verification.create(
          address_line1=addressLine1,
          address_line2=addressLine2,
          address_city=city,
          address_state=state,
          address_zip=zipCode, 
        )

address = verifiedAddress["address"]["address_line1"] + ", " + verifiedAddress["address"]["address_city"] + ", " + verifiedAddress["address"]["address_state"]
city = verifiedAddress["address"]["address_city"]
state = verifiedAddress["address"]["address_state"]


geocode_result = gmaps.geocode(address)

latitude = geocode_result[0]["geometry"]["location"]["lat"]
longitude = geocode_result[0]["geometry"]["location"]["lng"]

congressList = sunlight.congress.locate_legislators_by_lat_lon(latitude, longitude)

print "\n\nThanks for sharing your information! \nHere's some info about the current environment near " + address + ".\n"


f = urllib2.urlopen('http://api.wunderground.com/api/d13977cb92663c84/geolookup/conditions/q/' + state + "/" + city.replace(" ", "_") + '.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print "It's currently %s degrees in %s." %(temp_f, location)
f.close()

print "\n"
print "Here's a list of Congress members who represent your area: \n"

for rep in congressList:
    print rep["title"] + ". " + rep["first_name"] + " " + rep["last_name"]
    print rep["chamber"].capitalize()
    if rep["party"] == "R":
        print "Party: Republican"
    elif rep["party"] == "D":
        print "Party: Democrat"
    else:
        print rep["party"]
    print "Birthday: " + rep["birthday"]
    print rep["office"]
    print rep["phone"]
    print rep["oc_email"]
    print rep["state_name"]
    if rep["title"] == "Sen":
        print rep["state_rank"].capitalize()
    print "Term End: " + rep["term_end"]
    print "Term Start: " + rep["term_start"] 
    if rep["twitter_id"] != None:
        twitterId = rep["twitter_id"]
        print "Twitter ID: " + twitterId
        print "Latest Tweets: \n"
        public_tweets = api.user_timeline(screen_name=twitterId, count=20)
        for tweet in public_tweets:
            print tweet.text + "\n"

    print "\n"


