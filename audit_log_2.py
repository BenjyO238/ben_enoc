
#TODO: try catch
#TODO: optparse



from datetime import datetime
from datetime import time, timedelta, tzinfo
import time
import re, sys, os, csv



# files_to_process = os.listdir('./audit_files')


#Regex patterns:
# days = re.compile(r'Sun|Mon|Tue|Wed|Thu|Fri|Sat')
q = re.compile(r'"')
full_date = re.compile(r'\w\w\w\s+\w\w\w\s+[0-9]+') #3 char day 3 char month day num- signifies date of session
end_date_mark = re.compile(r'.*(\+|-)') #re.compile(r'.*\+')
session_line = re.compile(r'SESSION')
client_ip = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')     #(r'.+HOST=[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
user_id = re.compile(r'USERID:\[[0-9]+\]\s+"\w+"')
user_host = re.compile(r'USERHOST:\[[0-9]+\]\s+"[a-zA-Z.0-9]+"')#re.compile(r'USERHOST:\[[0-9]+\]\s+".*"')
os_user = re.compile(r'OS\$USERID:\[[0-9]+\]\s+"\w+"')
session_id = re.compile(r'SESSIONID:\[[0-9]+\]\s+"[0-9]+"')
return_code = re.compile(r'RETURNCODE:\[[0-9]+\]\s+"[0-9]+"')

#regex testing:
# print days.match('Saturday')
# print full_date.match('Tue Jul  2 05:17:03 2013 00:00+').span()
# print end_date_mark.match('Tue Jul  2 05:17:03 2013 00:00+').end()
# print client_ip.match('Client address: (ADDRESS=(PROTOCOL=tcp)(HOST=10.20.8.22)(PORT=59873)')
# print client_ip.search('Client address: (ADDRESS=(PROTOCOL=tcp)(HOST=10.20.8.22)(PORT=59873)').span() #use search not match to get proper start
# print session_line.match('SESSIONID:[9] "26741964')
# print user_host.search('STATEMENT:[1] "1" USERID:[10] "APP_SCHEMA" USERHOST:[23] "sumprdapp05.enernoc.net" TERMINAL:[7]').span()
# print os_user.search('OL=tcp)(HOST=10.20.10.155)(PORT=58571))" OS$USERID:[5] "jboss" DBID:[10] "1630961632" PRIV$USED:[1] "5"').span() #end marker not right
# print session_id.search('SESSIONID:[9] "269809099" ENTRYID:[1] "1" STATEMENT:[1] "1').span()
# print return_code.search('L:[7] "unknown" ACTION:[3] "100" RETURNCODE:[1] "0" COMMENT$TEXT:[99] "A').span()

###testing data file:
# log_file = open('./audit_files/prd2_ora_30626_4.aud', 'rb')
# log_f = log_file.read().split('\n')


FIELDS_TO_GRAB = [session_id, user_id, user_host, client_ip, os_user, return_code] #don't need full_date

def get_date_str(a_line):
    end_dt = end_date_mark.match(a_line).span() #get end of slice for date string
    return a_line[:int(end_dt[1]-2)] #end of date is second item in span tuple then subtract two spaces


def make_date(date_str):
    dt = time.strptime(date_str, '%a %b %d %H:%M:%S %Y')
    return dt


# print get_date_str(log_f)
# print make_date(get_date_str(log_f))


# def get_client_ip(a_line):
#     ip_str = client_ip.search(a_line).span()
#     return a_line[ip_str[0]:ip_str[1]]


# print get_client_ip(log_f)


def id_quotes(q_str):
    text = q_str
    start_quote = text.find('"')
    end_quote = text.rfind('"')
    quote_markers = (start_quote,end_quote)
    return quote_markers


# def get_user_id(a_line):
#     uid = user_id.search(a_line).span()
#     uid_str = a_line[uid[0]:uid[1]]
#     idq = id_quotes(uid_str)
#     return uid_str[idq[0]+1:idq[1]]


def get_field(a_line,reg_ex):
    field_test = reg_ex.search(a_line)
    if field_test: #if a match exists
        field_range = field_test.span()
        the_field = a_line[field_range[0]:field_range[1]]
        if q.search(the_field):   #there is a quote so need to call id_quotes
            idq = id_quotes(the_field)
            return the_field[idq[0]+1:idq[1]]
        else:
            return the_field
    else:
        return 'None'  #return string none if field is not present



##FIELDS_TO_GRAB = [session_id, user_id, user_host, client_ip, os_user, return_code]

def process_file(ora_log):
    entry = [] #holder for record
    field_regexs = FIELDS_TO_GRAB
    date_count = 0 #need to track counts to get only first entry of each element we need
    not_done = 0
    session_count = 0
    # ip_count = 0
    # user_count = 0
    for item in ora_log:
        if date_count == 0:
            if full_date.match(item):
                file_dt = get_date_str(item)
                entry.append(file_dt)
                date_count += 1
        elif date_count == 1 and not_done == 0:
            if session_line.match(item):
                session_count += 1 #don't return any entry if there is no "session"- it's not correct file format
                not_done += 1 #increment counter so we will stop processing file once we have data
                for fr in field_regexs:
                    field = get_field(item,fr) #apply regex for each field in list of regexes
                    entry.append(field)
                    print 'added ' + str(field) + ' to array.'
        else:
            pass
    if session_count == 1:
        return entry
    else:
        pass #don't return any data


# record = process_file(log_f)
# #
# print record



# record = process_file(log_f)
#
# print record






