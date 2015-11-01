import json

from _time import *

INPUT = 'schedule.json'

def main():

    with open(INPUT,'r') as infile:
        schedule = json.load(infile)

        weekday = 'NULL'
        while weekday not in WEEKDAYS:
            weekday = input('What day is it? ' )

        try:
            query = input('What time is it? ')

            date_time = datetime.datetime.strptime(query,FMT)
            date_time = date_time - datetime.timedelta(seconds = 60 * (date_time.minute % TIMESLOT))
            cur_time = date_time.strftime(FMT)

            print (sorted(schedule[weekday][cur_time]))

        except ValueError:
            print('Input a valid time in the format: '+FMT)
        except KeyError:
            print('Input a time between '+START_STR+' and '+END_STR)

if __name__ == "__main__":
    main()
