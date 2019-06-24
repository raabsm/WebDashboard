#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 23:54:00 2019

@author: samraab
"""
import tornado.ioloop
import tornado.web
import requests
import time
import logging
from tornado.log import enable_pretty_logging

WEATHER_API_KEY = "119f4ed0b5ca20d098497b54a430a6c3"

ZOMATO_API_KEY = "109136773c4244bb66745f4db5d67320"

AVIATION_API_KEY = "b918d5-5ab06e"  # only has 90 calls remaining!!!


def k2f(k):
    c = k - 273
    f = ((9 * c) / 5) + 32
    return f


def query_restaurant_data(lat, lon, city):
    location_url_from_lat_long = "https://developers.zomato.com/api/v2.1/locations?query=" + city + "&lat=" + str(
        lat) + "&lon=" + str(lon)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": ZOMATO_API_KEY}
    response = requests.get(location_url_from_lat_long, headers=header)
    rest_data = response.json()
    entity_type = rest_data['location_suggestions'][0]['entity_type']
    city_id = rest_data['location_suggestions'][0]['city_id']
    restaurant_url = "https://developers.zomato.com/api/v2.1/location_details?entity_id=" + str(
        city_id) + "&entity_type=" + entity_type
    start = time.time()
    response = requests.get(restaurant_url, headers=header)
    end = time.time()
    time_of_request = response.headers['Date']
    rest_data = response.json()
    num_restaurants = len(rest_data['best_rated_restaurant'])
    list_of_rest = []
    for num in range(0, num_restaurants):
        list_of_rest.append(rest_data['best_rated_restaurant'][num]['restaurant']['name'] + "--- location: "
                            + rest_data['best_rated_restaurant'][num]['restaurant']['location']['address'])
    return end - start, time_of_request, list_of_rest


def query_weather_data(city_name):
    start = time.time()
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=" + WEATHER_API_KEY)
    end = time.time()
    time_of_request = response.headers['Date']
    data = response.json()
    print(data)
    if data['cod'] != '200':
        print("ran error handler")
        logging.error("unable to query weather due to \"" + data['message'] + "\"")
        raise Exception(data['message'])
    else:
        weather_data = data['main']
        weather_city_id = data['id']
        humidity, pressure, temp_in_far, temp_max, temp_min = \
            weather_data['humidity'], weather_data['pressure'], k2f(weather_data['temp']), \
            k2f(weather_data['temp_max']), k2f(weather_data['temp_min'])
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        return end - start, time_of_request, weather_city_id, temp_in_far, temp_max, temp_min, humidity, pressure, latitude, longitude


def query_nearby_airports(lat, lon):
    url = "http://aviation-edge.com/v2/public/nearby?key=" + AVIATION_API_KEY + "&lat=" + str(lat) + "&lng=" + str(
        lon) + "&distance=50"
    start = time.time()
    response = requests.get(url)
    end = time.time()
    time_of_request = response.headers['Date']
    airport_data = response.json()
    list_of_airports = []
    for airport in airport_data:
        list_of_airports.append(
                                "Name of airport: " + airport['nameAirport'] + " Code: "
                                + airport['codeIataAirport'] + " City: "
                                + airport['codeIataCity'])
    return end - start, time_of_request, list_of_airports


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        handler = logging.FileHandler("logFile.txt")
        access_log = logging.getLogger("tornado.access")
        enable_pretty_logging()
        access_log.addHandler(handler)
        self.render('mainPage.html', error_message="")

    def post(self):
        user_input = self.get_body_argument("weather_city")
        try:
            weather_response_time, weather_request_time, weather_city_id, temp_in_far, temp_max, temp_min, humidity, pressure, latitude, longitude \
                = query_weather_data(user_input)
            rest_response_time, rest_request_time, rest_list \
                = query_restaurant_data(latitude, longitude, user_input)
            airport_response_time, airport_request_time, list_of_airports \
                = query_nearby_airports(latitude, longitude)
            self.render("weatherPage.html",
                        city_name=user_input,
                        weather_response_time=weather_response_time, weather_request_time=weather_request_time,
                        rest_response_time=rest_response_time, rest_request_time=rest_request_time,
                        cur_temp=temp_in_far, max_temp=temp_max, min_temp=temp_min, pressure=pressure,
                        humidity=humidity,
                        weather_city_id=weather_city_id,
                        items=rest_list,
                        airport_response_time=airport_response_time, airport_request_time=airport_request_time,
                        list_of_airports=list_of_airports)
        except Exception as e:
            error_message = ""
            if str(e) == 'city not found':
                error_message = '\"' + user_input + '\" is not a valid City.  Please try again'
            else:
                error_message = e
            self.render('mainPage.html', error_message=error_message)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
