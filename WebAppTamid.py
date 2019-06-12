#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 23:54:00 2019

@author: samraab
"""
import requests
import tornado.ioloop
import tornado.web

WEATHER_API_KEY = "119f4ed0b5ca20d098497b54a430a6c3"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('mainPage.html')
    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("weather_city"))
        message = self.get_body_argument("weather_city")
        r = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + message + "&appid=" + WEATHER_API_KEY) 
        data = r.json()
        print(data)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()