import os
import json
import pandas as pd
import requests
import time
import random
import requests
from googleplaces import GooglePlaces, geocode_location, types, lang
from dotenv import load_dotenv
from datetime import datetime
from urllib import response
import boto3

# Import environment variables
load_dotenv()
open_weather_key = os.getenv('OPEN_WEATHER_KEY')
open_weather_baseurl = os.getenv('OPEN_WEATHER_BASEURL')
aws_client = os.getenv('AWS_CLI_KEY')
aws_secret = os.getenv('AWS_CLI_SECRET')
places_client= os.getenv('PLACES_API_KEY')
google_places = GooglePlaces(places_client)
timestamp = time.strftime("%Y%m%d-%H%M%S")
office_file = os.getenv('OFFICE_FILE')
s3_bucket_name = "lunch-suggestion-system"

# Function which suggest lunch place near each office locations
def suggest_lunch_place(office_location):
     query_result = google_places.nearby_search(
     location= office_location,
     radius=3000,
     types=[types.TYPE_RESTAURANT])

    #return query_result
     rest_choice = (random.choice(query_result.places))
     rest_choice.get_details()
     rest_name = rest_choice.name
     rest_address = rest_choice.formatted_address
     rest_details = rest_choice.details
     rest_rating = rest_choice.rating
     global_phone_num = rest_choice.international_phone_number
     website = rest_choice.website
     url = rest_choice.url

    # Create dictionary which will contain data about the Office and Restaurant
     location_details= {  "Office location":  office_location, 
                                     "Restaurant suggestion": rest_name,
                                      "Restaurant address": rest_address,
                                      "Restaurant rating": rest_rating,
                                      "Restaurant website": website,
                                      "Restaurant phone": global_phone_num,
                                      "Url": url}
     
     geocode_location = fetch_geolocation (rest_address)
     lat = geocode_location [0]
     lng = geocode_location [1]
   
     weather_details = find_weather_data(lat, lng)
     data = merge_results (location_details, weather_details)
     return data

# Function which gives insight about weather conditions at the restaurant geo location
def find_weather_data(lat, lng):
    open_weather_url = 'https://api.openweathermap.org/data/2.5/weather?' + "lat=" + lat + "&lon=" + lng + "&appid=" + open_weather_key + "&units=metric"
    req = requests.get(open_weather_url)
    weather_data = req.json()
    
    weather_desc = weather_data["weather"][0]['description']
    temp = weather_data["main"]["temp"]
    temp_feels= weather_data["main"]["feels_like"]
    pressure = weather_data["main"]["pressure"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    weather_time = datetime.utcfromtimestamp(weather_data['dt'] + weather_data['timezone'])

    weather_details= {"Weather description": weather_desc,
                                      "Temperature feels like": temp_feels,
                                      "Pressure": pressure,
                                      "Humidity": humidity,
                                      "Wind Speed": wind_speed,
                                      "Time of Record": weather_time}
    return weather_details
  
def fetch_geolocation (rest_address):
 restaurant_geolocation = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+ rest_address + '&key=AIzaSyDmJkAbuMFs73fb44zNY21-cgytBOeUlNc')
 lat_lng = restaurant_geolocation.json()
 lat = lat_lng['results'][0]['geometry']['location']['lat']
 lng = lat_lng['results'][0]['geometry']['location']['lng']
 lat = str (lat)
 lng = str (lng)
 return lat, lng  

def merge_results(dict1, dict2):
  res = {**dict1, **dict2}
  return res
  
def upload_to_aws (file_name):
    s3 = boto3.client ('s3')
    with open (file_name, 'rb')  as f:
      s3.upload_fileobj(f, s3_bucket_name, file_name)
     
# Execute the main code     
if __name__ == '__main__':
  file_name="lss_" + timestamp + ".csv"
  with open("office.txt", encoding="utf8") as f:
     for line in f:
      office_location = f.readline()
      office_location = office_location.rstrip()
      lunch_suggestion_place = suggest_lunch_place(office_location)
      lss = pd.DataFrame([lunch_suggestion_place])
      
      # Create or update existing .csv file
      if os.path.isfile(file_name) : 
        lss.to_csv(file_name, mode='a', index=False, header=False)  
      else :
        lss.to_csv(file_name, index = False)  
        
# Upload .csv file to Amazon S3 (AWS)       
upload =  upload_to_aws (file_name)
