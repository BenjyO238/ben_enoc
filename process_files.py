__author__ = 'Orlowitz'

#TODO add optparse stuff for commandline
#TODO write to file then write to db
#TODO try except


import os, sys, re
import audit_log_2 as al


audit_dir = './audit_files' #directory of audit files



files_to_process = os.listdir(audit_dir)


def process_dir(audit_files):
    logins = {} #holder for records to write
    os.chdir(audit_dir)
    for file in audit_files:
        log_file = open(file, 'rb')
        log_f = log_file.read().split('\n')
        data = al.process_file(log_f)
        logins[file] = data
        log_file.close()
    return logins


log_entries = process_dir(files_to_process)


log_in_data = open('audit_login_data', 'w')


for key, value in log_entries.items():
    # print key, value
    if value:
        line = [str(key), value[0].strftime("%Y-%m-%d %H:%M:%S"), str(value[1]), str(value[2])]
        # print line
        w_line = '%s, %s, %s,%s' % (line[0],line[1],line[2],line[3])
        log_in_data.write(w_line + '\n')

log_in_data.close()


