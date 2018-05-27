
# coding: utf-8

# In[17]:


import csv
import numpy as np
from collections import Counter
import time
from datetime import datetime, timedelta
from itertools import groupby
import operator

File4 = []
a = []
item = 0
File = []
File2 = []
File3 = []
ip = []
end = []
Final_sess1 = []
Final_sess2 = []
Final_sess3 = []
Final = []

# open input file and count requests with id, grouping id regardless of session
with open('/Users/christianbeynis/Desktop/Github/Edgar-Analytics/input/log.csv', 'rt') as f:
    
    reader = csv.reader(f)
    next(reader, None)
    for key, group in groupby(reader, lambda x: (x[2],x[0])):
        for thing in group:
            File.append(key)
    File2 = Counter(File)
    for k,v in Counter(File).items():
        ip.append([k,v])       
        
f.close()

#Retrieve the date
with open('/Users/christianbeynis/Desktop/Github/Edgar-Analytics/input/log.csv', 'rt') as f:
    next(f)
    date = f.readline().split(',')[1]
    date = datetime.strptime(date, '%m/%d/%y')
    date.strftime('%Y-%m-%d') 
    f.close()

# Retrieve the final time and convert into date format
t_final = File[-1:][0][0]
t_final_s = 360*int(t_final[:1])+60*int(t_final[2:4])+int(t_final[5:])
T_final = date + timedelta(seconds= t_final_s)

#find inactivity time
t_inac1 = open('/Users/christianbeynis/Desktop/Github/Edgar-Analytics/input/inactivity_period.txt','r')
t_inac = int(t_inac1.read())
t_inac1.close()

# id and session time from the begining in seconds, requests                       
values = set(map(lambda x:x[0][1], ip))
File3 = [[[360*int(y[0][0][:1])+60*int(y[0][0][2:4])+int(y[0][0][5:]),y[1], y[0][1]] for y in ip if y[0][1]==x] for x in values]                     

# separate sessions according to activity
for item in range(len(File3)):
    a.append(np.diff([pair[0] for pair in File3[item]]))

    if len(a[item]) != 0:
        for value in range(len(a[item])):
            File3[item][value+1][0] = a[item][value]
                
for item in range(len(File3)):
    for element in range(len(File3[item])):
        if element >0 and File3[item][element][0] > t_inac :
                File4.append([File3[item][element-1]])
                File4.append([File3[item][element]])
                File3[item][element][0] = File3[item][element][0] + 1
        else:
            if element == len(File3[item]) - 1:
                 File4.append(File3[item])             

# end is the file with id t initial, t final, duration, request with 1 second inclusive
for item2 in range(len(File4)):
    end.append([File4[item2][0][2],
                date + timedelta(seconds=int(File4[item2][0][0])),
                (sum(t for t, Req, id_ in File4[item2])+1-File4[item2][0][0]),
                (sum(Req for t, Req, id_ in File4[item2]))])
        


# ordering for session finishing before final time,
# the one that would eventually or not finish at the final time.
# They are active 2s before the end of session
# session active that are stopped at the final time, they pull a request
for item in range(len(end)):
    t_i = end[item][1]
    t_f = end[item][1] + timedelta(seconds= int(end[item][2])-1)
    if  t_f + timedelta(seconds= t_inac) < T_final:
        Final_sess1.append([end[item][0],t_i, t_f,end[item][2], end[item][3]])
    else:
        if t_f < T_final:
            Final_sess2.append([end[item][0],t_i, t_f,end[item][2], end[item][3]])
        else:
            Final_sess3.append([end[item][0],t_i, t_f,end[item][2],end[item][3]])

#sorting and regrouping of all cases lists
Final_sess1 = sorted(Final_sess1, key=operator.itemgetter(2))
Final_sess2 = sorted(Final_sess2, key=operator.itemgetter(1))
Final_sess3 = sorted(Final_sess3, key=operator.itemgetter(1))
Final = Final_sess1 + Final_sess2 + Final_sess3


#write file
sessionization  = open('/Users/christianbeynis/Desktop/Github/Edgar-Analytics/insight_testsuite/temp/output/sessionization.txt', 'w')
for lines in range(len(Final)):
    for itemized in range(len(Final[lines])):
        sessionization.write(str(Final[lines][itemized]))
        if itemized+1 != len(Final[lines]) :
            sessionization.write(',')
    if lines-1 != len(Final):
        sessionization.write('\n')
    
sessionization.close()

