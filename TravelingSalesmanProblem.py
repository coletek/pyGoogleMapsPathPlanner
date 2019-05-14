import sys
import csv
import googlemaps
import pprint
from datetime import datetime

YOUR_API_KEY = sys.argv[1]
start_address = sys.argv[2]
end_address = sys.argv[3]
stops_filename = sys.argv[4]

addresses = []

gmaps = googlemaps.Client(YOUR_API_KEY)
pp = pprint.PrettyPrinter(indent=4)

data = {}

with open(stops_filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        address = row[0]
        addresses.append(address)
        geocode_result = gmaps.geocode(address)
        formatted_address = geocode_result[0]['formatted_address']
        data[formatted_address] = {'address': row[0],
                                   'name': row[1].strip(),
                                   'phone': row[2].strip(),
                                   'email': row[3].strip()}
        
#print addresses

now = datetime.now()
directions_result = gmaps.directions(origin=start_address,
                                     destination=end_address,
                                     waypoints=addresses,
                                     optimize_waypoints=True,
                                     mode="driving",                                     
                                     departure_time=now)


geocode_result = gmaps.geocode(end_address)
formatted_end_address = geocode_result[0]['formatted_address']

duration_total = 0.0
for legs in directions_result[0]['legs']:
    address = legs['end_address']
    distance = legs['distance']['text']
    duration = legs['duration']['text']
    duration_total = duration_total + float(legs['duration']['value'])
    if formatted_end_address != address:
        name = data[address]['name']
        phone = data[address]['phone']
        email = data[address]['email']
        print ("%s %s %s" % (name, phone, email))
    print ("%s: %s %s" % (address, distance, duration))
    print ("")

stops = len(directions_result[0]['legs'])
print ("count: %d" % (stops))
print ("driving duration (est): %.1fhrs" % (round(duration_total / 60 / 60, 2)))
print ("trip duration (est): %.1fhrs" % (round(duration_total / 60 / 60, 2) + (stops - 1) * 0.5))
