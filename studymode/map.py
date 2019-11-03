import geocoder
from flask_googlemaps import Map, icons


def draw_map():
    g = geocoder.ip('me')
    latitude, longitude = g.latlng[0], g.latlng[1]

    studymap = Map(
        identifier="study",
        varname="studymap",
        style="height:720px;width:1100px;margin:0;",
        lat=latitude,
        lng=longitude,
        zoom=15,
        markers=[(37.4419, -122.1419)]
    )
    return studymap



