#TODO: try catch
#TODO: optparse



from datetime import datetime
from datetime import time, timedelta, tzinfo

import re, sys, os, json, string, csv



files_to_process = os.listdir('./audit_files')

'''
def print_me(p):
    print p

[print_me(file) for file in files_to_process]
'''

#Regex patterns:
# days = re.compile(r'Sun|Mon|Tue|Wed|Thu|Fri|Sat')
full_date = re.compile(r'\w\w\w\s+\w\w\w\s+[0-9]+') #3 char day 3 char month day num- signifies date of session
end_date_mark = re.compile(r'.*\+')
session_line = re.compile(r'SESSION')
client_ip = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')     #(r'.+HOST=[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
user_id = re.compile(r'USERID:\[[0-9]+\]\s+"\w+"')

# print days.match('Saturday')
# print full_date.match('Tue Jul  2 05:17:03 2013 00:00+').span()
# print end_date_mark.match('Tue Jul  2 05:17:03 2013 00:00+').end()
# print client_ip.match('Client address: (ADDRESS=(PROTOCOL=tcp)(HOST=10.20.8.22)(PORT=59873)')
# print client_ip.search('Client address: (ADDRESS=(PROTOCOL=tcp)(HOST=10.20.8.22)(PORT=59873)').span() #use search not match to get proper start
# print session_line.match('SESSIONID:[9] "26741964')


log_file = open('./audit_files/prd1_ora_5618_1.aud', 'rb')
log_f = log_file.read().split('\n')


# '''
for i, item in enumerate(log_f):
    print str(i) + ', ' + item
# '''



def get_date_str(ora_log):
    for item in ora_log:
        if full_date.match(item):
            end_dt = end_date_mark.match(item).span() #get end of slice for date string
            return item[:int(end_dt[1]-2)] #end of date is second item in span tuple then subtract two spaces
        else:
            pass


def make_date(date_str):
    dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
    return dt


# print get_date_str(log_f)
print make_date(get_date_str(log_f))


def get_client_ip(ora_log):
    for item in ora_log:
        if session_line.match(item):
            if client_ip.search(item):
                ip_str = client_ip.search(item).span()
                return item[ip_str[0]:ip_str[1]]

print get_client_ip(log_f)


def id_quotes(q_str):
    text = q_str
    start_quote = text.find('"')
    end_quote = text.rfind('"')
    quote_markers = (start_quote,end_quote)
    return quote_markers


def get_user_id(ora_log):
    for item in ora_log:
        if session_line.match(item):
            if user_id.search(item):
                uid = user_id.search(item).span()
                uid_str = item[uid[0]:uid[1]]
                idq = id_quotes(uid_str)
                return uid_str[idq[0]+1:idq[1]]


print get_user_id(log_f)









