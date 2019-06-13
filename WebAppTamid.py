#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 23:54:00 2019

@author: samraab
"""
import requests
import tornado.ioloop
import tornado.web
import requests
from pprint import pprint


WEATHER_API_KEY = "119f4ed0b5ca20d098497b54a430a6c3"

ZOMATO_API_KEY = "109136773c4244bb66745f4db5d67320"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('mainPage.html')
    def post(self):
        #self.render('weatherPage.html')
        message = self.get_body_argument("weather_city")
        temp,lat,lon = self.queryWeatherData(message)
        print("temp in " + message + "is", temp)
        self.queryRestaurantData(lat, lon, message)
    def queryWeatherData(self, cityName):
    	r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + WEATHER_API_KEY) 
    	data = r.json()
    	pprint(data)
    	tempInFar = self.k2f(data['main']['temp'])
    	latitude = data['coord']['lat']
    	longitude = data['coord']['lon']
    	return tempInFar, latitude, longitude
    def queryRestaurantData(self, lat, lon, city):
    	locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/locations?query=" + city + "&lat=" + str(lat) + "&lon=" + str(lon)
    	header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": ZOMATO_API_KEY}
    	response = requests.get(locationUrlFromLatLong, headers=header)
    	restData = response.json()
    	entity_type = restData['location_suggestions'][0]['entity_type']
    	city_id = restData['location_suggestions'][0]['city_id']
    	print("restaurant info:", entity_type, city_id)
    	restaurantURL = "https://developers.zomato.com/api/v2.1/location_details?entity_id=" + str(city_id)+ "&entity_type=" + entity_type 
    	response = requests.get(restaurantURL, headers=header)
    	restData = response.json()
    	numRestaurants = len(restData['best_rated_restaurant'])
    	print("numRestaurants", numRestaurants)
    	for num in range(0,numRestaurants):
    		print(restData['best_rated_restaurant'][num]['restaurant']['name'], restData['best_rated_restaurant'][num]['restaurant']['location']['address'])


    def k2f(self, k):
    	c = k - 273
    	f = ((9 * c) / 5) + 32
    	return f



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()