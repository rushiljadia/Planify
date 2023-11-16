import urllib
import json

"""Using https://geocode.maps.co/"""

response = urllib.request.urlopen(
    "https://geocode.maps.co/search?q=J.+Murrey+Atkins+Library"
)
dict = json.load(response)
print(dict)
