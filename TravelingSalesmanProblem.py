import sys
import csv
import googlemaps
import pprint
from datetime import datetime

YOUR_API_KEY = sys.argv[1]
start_address = sys.argv[2]
end_address = sys.argv[3]
stops_filename = sys.argv[4]
start_time = float(sys.argv[5])
#stop_time = float(sys.argv[6])

addresses = []

gmaps = googlemaps.Client(YOUR_API_KEY)
pp = pprint.PrettyPrinter(indent=4)

data = {}

with open(stops_filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        address = row[1].strip()
        addresses.append(address)
        geocode_result = gmaps.geocode(address)
        formatted_address = geocode_result[0]['formatted_address']
        data[formatted_address] = {'stop_time': row[0].strip(),
                                   'address': address,
                                   'name': row[2].strip(),
                                   'phone': row[3].strip(),
                                   'email': row[4].strip()}
        
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

eta = start_time * 60.0 * 60.0
driving_total = 0.0
duration_total = 0.0
for legs in directions_result[0]['legs']:
    address = legs['end_address']
    distance = legs['distance']['text']
    duration = legs['duration']['text']
    if formatted_end_address != address:
        name = data[address]['name']
        phone = data[address]['phone']
        email = data[address]['email']
        stop_time = float(data[address]['stop_time']) * 60 * 60
        print ("Contact Details: %s %s %s" % (name, phone, email))
    eta += legs['duration']['value']
    print ("Address: %s" % (address))
    print ("Duration: %s, %s" % (distance, duration))
    print ("ETA: %.2f" % (eta / 60.0 / 60.0))
    if formatted_end_address != address:
        print ("Stop Time: %.2fhr" % (stop_time / 60.0 / 60.0))
    print ("")
    #if formatted_end_address != address:
    #    duration_total += stop_time * 3600
    driving_total += legs['duration']['value']
    eta += stop_time
    
stops = len(directions_result[0]['legs'])
print ("# of stops: %d" % (stops))
print ("driving duration (est): %.1fhrs" % (driving_total / 60.0 / 60.0))
print ("trip duration (est): %.1fhrs" % ((eta - start_time * 60.0 * 60.0) / 60.0 / 60.0))
