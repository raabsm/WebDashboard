#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 23:54:00 2019

@author: samraab
"""
import requests
import tornado.ioloop
import tornado.web
from tornado import template
import requests
from pprint import pprint
import time 


WEATHER_API_KEY = "119f4ed0b5ca20d098497b54a430a6c3"

ZOMATO_API_KEY = "109136773c4244bb66745f4db5d67320"

def k2f(k):
	c = k - 273
	f = ((9 * c) / 5) + 32
	return f


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('mainPage.html')
    def post(self):
        #self.render('weatherPage.html')
        message = self.get_body_argument("weather_city")
        weather_response_time, weather_request_time, weather_city_id, tempInFar, temp_max, temp_min, humidity, pressure, latitude, longitude = self.queryWeatherData(message)
        rest_response_time, rest_request_time, restList = self.queryRestaurantData(latitude, longitude, message)
        self.render("weatherPage.html", 
			city_name = message, 
        	weather_response_time = weather_response_time, weather_request_time = weather_request_time, 
        	rest_response_time = rest_response_time, rest_request_time = rest_request_time, 
        	cur_temp = tempInFar, max_temp = temp_max, min_temp = temp_min, pressure = pressure, humidity = humidity, weather_city_id = weather_city_id, 
        	items = restList)
    def queryWeatherData(self, cityName):
    	start = time.time()
    	r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + WEATHER_API_KEY) 
    	end = time.time()
    	timeOfRequest = r.headers['Date']
    	data = r.json()
    	weather_data = data['main']
    	weather_city_id = data['id']
    	humidity, pressure, tempInFar, temp_max, temp_min = weather_data['humidity'], weather_data['pressure'],k2f(weather_data['temp']),k2f(weather_data['temp_max']),k2f(weather_data['temp_min']) 
    	latitude = data['coord']['lat']
    	longitude = data['coord']['lon']
    	return end-start, timeOfRequest, weather_city_id, tempInFar, temp_max, temp_min, humidity, pressure, latitude, longitude
    def queryRestaurantData(self, lat, lon, city):
    	locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/locations?query=" + city + "&lat=" + str(lat) + "&lon=" + str(lon)
    	header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": ZOMATO_API_KEY}
    	response = requests.get(locationUrlFromLatLong, headers=header)
    	restData = response.json()
    	entity_type = restData['location_suggestions'][0]['entity_type']
    	city_id = restData['location_suggestions'][0]['city_id']
    	restaurantURL = "https://developers.zomato.com/api/v2.1/location_details?entity_id=" + str(city_id)+ "&entity_type=" + entity_type 
    	start = time.time()
    	response = requests.get(restaurantURL, headers=header)
    	end = time.time()
    	timeOfRequest = response.headers['Date']
    	restData = response.json()
    	numRestaurants = len(restData['best_rated_restaurant'])
    	listOfRest = []
    	for num in range(0,numRestaurants):
    		listOfRest.append(restData['best_rated_restaurant'][num]['restaurant']['name'] + "--- location: " + restData['best_rated_restaurant'][num]['restaurant']['location']['address'])
    	return end-start, timeOfRequest, listOfRest




def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()