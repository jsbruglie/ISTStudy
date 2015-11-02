import json
import requests
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

            response = requests.get(ENDPOINT + id +'/', {DAY : DATE})
            jsonData = json.loads(response.text)

            # Initialization of the dict
            events = dict((weekday,list()) for weekday in WEEKDAYS)

            try:
                # Create temp struct for event data storag
                for event in jsonData['events']:
                    if event['weekday'] not in WEEKDAYS_AVOID:
                        if event['end'] > END_STR:
                            event['end'] = END_STR

                        events[event['weekday']].append(event['start']+'-'+event['end'])

                for weekday in WEEKDAYS:
                    events[weekday] = sorted(events[weekday])

                    current = START

                    for event in events[weekday]:
                        start_str, end_str = event.split('-')
                        start = datetime.datetime.strptime(start_str,FMT)
                        end = datetime.datetime.strptime(end_str,FMT)

                        for single_time in minutesRange(current,end,TIMESLOT):
                            single_time_duration = single_time + datetime.timedelta(seconds=60*TIMESLOT)

                            if isNotContained(single_time,single_time_duration,start,end):
                                final[weekday][single_time.strftime(FMT)].append(name)

                        current = end

                    for single_time in minutesRange(current,END,TIMESLOT):
                        final[weekday][single_time.strftime(FMT)].append(name)

            except KeyError:
                print(name)
                pass

        with open(OUTPUT,'w') as out:
            json.dump(final, out, sort_keys=True,indent=4, separators=(',', ': '))
            out.close()

        quit()

if __name__ == "__main__":
    main()
