__author__ = 'Orlowitz'

#TODO write to file then write to db
#TODO try except


import os, sys, re
import audit_log_2 as al
# import optparse
import shutil
from datetime import datetime
import time



#command line stuff
# parser = optparse.OptionParser()
# parser.add_option('-d', help='audit file directory', dest='audit_dir')

# (opts, args) = parser.parse_args()

audit_dir = sys.argv[1] #opts.audit_dir #'./audit_files' #opts.audit_dir #'./audit_files' #directory of audit files
current_dir = os.getcwd()
files_to_process = os.listdir(audit_dir)
files_to_process = [f for f in files_to_process if f[-3:] == 'aud'] #get only aud files
# print files_to_process



def process_dir(audit_dir):
    logins = {} #holder for records to write
    os.chdir(audit_dir)
    for file in files_to_process:
        log_file = open(file, 'rb')
        log_f = log_file.read().split('\n')
        data = al.process_file(log_f)
        logins[file] = data
        log_file.close()
    os.chdir(current_dir)
    return logins

# l = process_dir(audit_dir)
# print l



#TODO use make_dir and append to file name to write separate files if too big
def write_entries():
    os.chdir(current_dir)
    try:
        log_in_data = open('./audit_login_data.txt', 'a')
    except IOError:
        log_in_data = open('./audit_login_data.txt', 'w')

    log_entries = process_dir(audit_dir)

    for key, value in log_entries.items():
        # print key, value
        if value:
            line = str(key)
            #val_str = [str(v) for v in value] #ensure the values are strings for later writing to file
            more_line = ",".join(value)
            # print line
            w_line = line +',' + more_line
            log_in_data.write(w_line + '\n')

    log_in_data.close()

# write_entries()


def make_dir():
    n = datetime.now()
    new_d = '%s%s%s%s%s%s' % (str(n.year), str(n.month),str(n.day),str(n.hour),str(n.minute), str(n.second))
    return new_d


def move_completed_files(files_to_move):
    os.chdir(current_dir)
    dir_name = make_dir()
    new_dir = current_dir + '/processed_audit_files/'+ dir_name
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    os.chdir(audit_dir)

    files = files_to_move

    for file in files:
        shutil.move(file, new_dir)
    os.chdir(current_dir)

#TODO filter unwanted users
def main():
    write_entries()
    print 'Done writing entries. Now moving files.'
    move_completed_files(files_to_process) #move files once processed.
    print 'Done processing audit files'


if __name__ == '__main__':
    main()



