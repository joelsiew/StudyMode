import geocoder
from flask_googlemaps import Map
from flask import render_template
import requests
import json

def draw_map(events):
    g = geocoder.ip('me')
    latitude, longitude = g.latlng[0], g.latlng[1]
    markers_list = make_markers(events)
    studymap = Map(
        identifier="study",
        varname="studymap",
        style="height:100%;width:100%;margin:0;",
        lat=latitude,
        lng=longitude,
        zoom=15,
        markers=markers_list
    )
    return studymap


def make_markers(events):
    markers = []
    for event in events:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=AIzaSyBq_qn6etPVIO8OZVTvPHtk7JMCriN04wQ".format(event.latitude, event.longitude))
        json_data = json.loads(response.text)
        event_details = {
            'lat': event.latitude,
            'lng': event.longitude,
            'infobox': render_template('marker.html', event=event, json_data=json_data)
        }
        markers.append(event_details)
    return markers
