import geocoder
from flask_googlemaps import Map, icons
from studymode.models import User, Event


def draw_map(events):
    g = geocoder.ip('me')
    latitude, longitude = g.latlng[0], g.latlng[1]
    markers_list = make_markers(events)
    markers_list.append({'lat': 30.267153, 'lng': -97.743057, 'infobox': "Fam squad"})
    print(markers_list)
    studymap = Map(
        identifier="study",
        varname="studymap",
        style="height:720px;width:480px;margin:0;",
        lat=latitude,
        lng=longitude,
        zoom=15,
        markers=markers_list
    )
    return studymap


def make_markers(events):
    markers = []
    for event in events:
        event_details = {
            'lat': event.latitude,
            'lng': event.longitude,
            'infobox': event.class_name
        }
        markers.append(event_details)
    return markers
