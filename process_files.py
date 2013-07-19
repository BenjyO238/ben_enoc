__author__ = 'Orlowitz'


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
        logins[file] = al.process_file(file)
        log_file.close()
    return logins


log_entries = process_dir(files_to_process)


print log_entries




