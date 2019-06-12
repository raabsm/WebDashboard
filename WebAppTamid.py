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

config={
  "user_key":"109136773c4244bb66745f4db5d67320"
  }

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('mainPage.html')
    def post(self):
        #self.write("You wrote " + self.get_body_argument("weather_city"))
        self.render('weatherPage.html')

        # message = self.get_body_argument("weather_city")
        # r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + message + "&appid=" + WEATHER_API_KEY) 
        # data = r.json()
        # temp = data['main']['temp']
        # c = temp - 273
        # f = ((9 * c) / 5) + 32
        # print("temp", f)
        # locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/geocode?lat=40.74&lon=-74.17"
        # header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "109136773c4244bb66745f4db5d67320"}
        # response = requests.get(locationUrlFromLatLong, headers=header)
       # print("json response for Zomato:")
       # pprint(response.json())

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()