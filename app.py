import json
import re
import sys

from _time import *

INPUT = 'schedule.json'
OPTIONS = 'Options:\n r-[Room] : Checks the availability of a single room\n t-[Time] : Returns a list of every room available in the current time slot\n [Any other command] : Exit the program'
GREETING ='\n██╗███████╗████████╗███████╗████████╗██╗   ██╗██████╗ ██╗   ██╗\n██║██╔════╝╚══██╔══╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗╚██╗ ██╔╝\n██║███████╗   ██║   ███████╗   ██║   ██║   ██║██║  ██║ ╚████╔╝ \n██║╚════██║   ██║   ╚════██║   ██║   ██║   ██║██║  ██║  ╚██╔╝  \n██║███████║   ██║   ███████║   ██║   ╚██████╔╝██████╔╝   ██║   \n╚═╝╚══════╝   ╚═╝   ╚══════╝   ╚═╝    ╚═════╝ ╚═════╝    ╚═╝\n'

def main():

    with open(INPUT,'r') as infile:
        schedule = json.load(infile)

        print(GREETING)

        weekday = 'NULL'
        while weekday not in WEEKDAYS:
            weekday = input('What day of the week is it? ' )

        try:
            print(OPTIONS)

            while True:

                option, query = input('>>').split('-')
                if option == 't':
                    date_time = datetime.datetime.strptime(query,FMT)
                    date_time = date_time - datetime.timedelta(seconds = 60 * (date_time.minute % TIMESLOT))
                    cur_time = date_time.strftime(FMT)
                    array = sorted(schedule[weekday][cur_time])
                    for entry in array:
                        name, timeslots = entry.split('-')
                        time = datetime.datetime.strptime('00:00',FMT)
                        time = time + datetime.timedelta(seconds = 60 * TIMESLOT * int(timeslots))
                        time_available = time.strftime(FMT)
                        print (name+': available now and in the next \t'+timeslots+' timeslots \t('+time_available+')')
                elif  option  == 'r':
                    for single_time in minutesRange(START,END,TIMESLOT):
                        for entry in schedule[weekday][single_time.strftime(FMT)]:
                            room, timeslots = entry.split('-')
                            if room == query:
                                timeslots = int(timeslots) + 1
                                time = datetime.datetime.strptime('00:00',FMT)
                                time = time + datetime.timedelta(seconds = 60 * TIMESLOT * timeslots)
                                time_available = time.strftime(FMT)
                                print('Available from '+single_time.strftime(FMT)+' for '+str(timeslots)+' timeslots ('+time_available+')')
                else:
                    print(OPTIONS)
                    quit()
        except ValueError:
            pass
        except KeyError:
            print('Input a time between '+START_STR+' and '+END_STR)

if __name__ == "__main__":
    main()
