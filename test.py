import urllib2
import json

city = "Washington"
state = "DC"

f = urllib2.urlopen('http://api.wunderground.com/api/d13977cb92663c84/geolookup/conditions/q/' + state + "/" + city.replace(" ", "_") + '.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print "Current temperature in %s is: %s" % (location, temp_f)
f.close()