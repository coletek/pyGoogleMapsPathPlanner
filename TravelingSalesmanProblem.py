import sys
import csv
import googlemaps
from datetime import datetime

YOUR_API_KEY = sys.argv[1]
start_address = sys.argv[2]
end_address = sys.argv[3]
stops_filename = sys.argv[4]

addresses = []

with open(stops_filename, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        addresses.append(row[0])

#print addresses

gmaps = googlemaps.Client(key=YOUR_API_KEY)

now = datetime.now()
directions_result = gmaps.directions(origin=start_address,
                                     destination=end_address,
                                     waypoints=addresses,
                                     optimize_waypoints=True,
                                     mode="driving",                                     
                                     departure_time=now)


duration = 0.0
for legs in directions_result[0]['legs']:
        duration = duration + float(legs['duration']['value'])
        print legs['end_address'] + ": " + legs['distance']['text'] + " " + legs['duration']['text']
        print ""

stops = len(directions_result[0]['legs'])
print ("count: %d" % (stops))
print ("driving duration (est): %.1fhrs" % (round(duration / 60 / 60, 2)))
print ("trip duration (est): %.1fhrs" % (round(duration / 60 / 60, 2) + (stops - 1) * 0.5))
