# Edgar_Analytics

Edgar Analytics Challenge.

Algorithm:

The part between ‘{}’ is not coded:

{While data are being collected, the following commands start when we the amount of data have reached a given cutoff number. We then ‘sessionize’ iteratively each subfiles and later join them}

To ‘sessionize’ our data:

- We open the file input file log.csv, retrieve the date once (the SEC files are classified by date), we convert the date to the desired format. We assume each session is contained within the same day.
-We retrieve each log and group by ip and time to gives a count of the request at time t (File and File2) [we use groupby and counter]
-We store the final time for the session converted in date time format.
-We open the input inactivity_period.txt to obtain t_inac = 2
-With set map, for each ip we associate in the following format [time of request, number of request, ip]
-We ‘sessionize’ our ip according to the inactivity time 
   1/ We compute the time of time of inactivity from File3 with the diff() function. 
   2/ We create a record for this in File3 (2nd for loop)
   3/ We separate each  list session that has time of inactivity greater than 2 by separating into two lists with same ip (3rd loop)
This is File4.
-From File4 we create file end by appending 
[ip, starting time in datetime format, ending time in date time format, duration through summation of times in File4 in 1s inclusive, Request number through summation]

-We separate our sessions between the ones that end before the end of all sessions, the ones 
active before its end and the one active and requesting at the final time.  This gives us three Final_sess

- We use the function sort and choose the parameter accordingly for itemgetter
- We Join our list to yield the sorted final session log summary. This is the file Final
- We create the file sessionization.txt and write the summary logs.

The code is written in Python 3.6

The we use the standard libraries:

- csv
- numpy
- collections, counter
- time
- date time, timedelta
- itertools, groupby
- operator
