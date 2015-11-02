import json
import re

from _time import *

INPUT = 'schedule.json'
OPTIONS = 'Options:\n r-[Room] : Checks the availability of a single room\n t-[Time] : Returns a list of every room available in the current time slot'

def main():

    with open(INPUT,'r') as infile:
        schedule = json.load(infile)

        weekday = 'NULL'
        while weekday not in WEEKDAYS:
            weekday = input('What day of the week is it? ' )

        try:

            print(OPTIONS)
            while True:

                option, query = input('\n>>').split('-')
                if option == 't':
                    date_time = datetime.datetime.strptime(query,FMT)
                    date_time = date_time - datetime.timedelta(seconds = 60 * (date_time.minute % TIMESLOT))
                    cur_time = date_time.strftime(FMT)
                    print (sorted(schedule[weekday][cur_time]))
                elif  option  == 'r':
                    for single_time in minutesRange(START,END,TIMESLOT):
                        for room in schedule[weekday][single_time.strftime(FMT)]:
                            if room == query:
                                print(room+' '+single_time.strftime(FMT))
                else:
                    print(OPTIONS)
                    quit()
        except ValueError:
            print(OPTIONS)
        except KeyError:
            print('Input a time between '+START_STR+' and '+END_STR)

if __name__ == "__main__":
    main()
