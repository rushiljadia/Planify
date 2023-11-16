import urllib
import json
import datetime


def get_distance():
    map_key = "pk.eyJ1Ijoia2FwaGVscHMzMyIsImEiOiJjbG9xOHJoczEwZzd3MmttY2E1azIxMDE2In0.6aYFPziyzO_qDoSY4zIpIQ"

    url = f"https://api.mapbox.com/directions/v5/mapbox/walking/-80.734458%2C35.304643%3B-80.735615%2C35.305276?access_token={map_key}"

    response = urllib.request.urlopen(url)

    dict = json.load(response)

    print(dict["routes"][0]["duration"] / 60)

    distance = datetime.timedelta(seconds=dict["routes"][0]["duration"])

    return distance
