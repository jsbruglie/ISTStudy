import datetime

def minutesRange(start,end,delta):

	time_delta = end-start
	max_range = int(time_delta.seconds/(60*delta))
	for i in range (max_range):
		yield  start + datetime.timedelta(seconds=i*60*delta)

def isNotContained(start1,end1,start2,end2):

	# start2 - start1 <= 0 if start2 <= start1
	a = start2 - start1
	# end2 - end1 >= 0 if end2 >= end1
	b = end2 - end1
	return not (a.total_seconds() <= 0 and b.total_seconds() >= 0)
