import json
import urllib.request
import csv
from pprint import pprint
from collections import defaultdict

from _time import *

ENDPOINT = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
INPUT = 'spaces.csv'
OUTPUT = 'schedule.json'

KEYS = []
for single_time in minutesRange(START,END,TIMESLOT):
    KEYS.append(single_time.strftime(FMT))

def main():

    with open(INPUT, mode='r') as infile:

        final = dict((weekday,[]) for weekday in WEEKDAYS)
        for weekday in WEEKDAYS:
            final[weekday] = defaultdict(list)
            for key in KEYS:
                final[weekday].setdefault(key, [])

        reader = csv.DictReader(infile)
        for row in reader:

            path, name, id = row['path'], row['name'], row['id']

            request = ENDPOINT + id +'/?'+DAY+'='+DATE
            response = urllib.request.urlopen(request)
            str_response = response.readall().decode('utf-8')
            jsonData = json.loads(str_response)

            # Initialization of the dict
            events = dict((weekday,list()) for weekday in WEEKDAYS)

            try:
                # Create a temp struct for event data storage
                for event in jsonData['events']:
                    if event['weekday'] not in WEEKDAYS_AVOID:
                        if event['end'] > END_STR:
                            event['end'] = END_STR

                        events[event['weekday']].append(event['start']+'-'+event['end'])

                for weekday in WEEKDAYS:

                    # Temp structure used to store whether the room will be free or not in each of the timeslots
                    temp = dict.fromkeys(KEYS)

                    # Sort the event array by time (alphabetically)
                    events[weekday] = sorted(events[weekday])
                    current = START

                    # Iterate through each of the events for a certain room, by weekday
                    for event in events[weekday]:
                        start_str, end_str = event.split('-')
                        start = datetime.datetime.strptime(start_str,FMT)
                        end = datetime.datetime.strptime(end_str,FMT)

                        for single_time in minutesRange(current,end,TIMESLOT):
                            single_time_duration = single_time + datetime.timedelta(seconds=60*TIMESLOT)

                            # If the timeslot evaluated is not within the limits of the current event
                            if isNotContained(single_time,single_time_duration,start,end):
                                temp[single_time.strftime(FMT)] = True

                        current = end

                    # Account for availability after all the events
                    for single_time in minutesRange(current,END,TIMESLOT):
                        temp[single_time.strftime(FMT)] = True

                    # Go through the events in reverse order in order to determine for how much more timeslots the room will be free
                    keys_inv = sorted(KEYS,reverse=True)
                    counter = 0
                    for time_str in keys_inv:
                        if temp[time_str]:
                            final[weekday][time_str].append(name+'-'+str(counter))
                            counter +=1
                        else:
                            counter=0

            except KeyError:
                print("There's probably something wrong with the JSON data. Are you sure all of the room id's are correct?")

        with open(OUTPUT,'w') as out:
            json.dump(final, out, sort_keys=True,indent=4, separators=(',', ': '))
            out.close()

        quit()

if __name__ == "__main__":
    main()
