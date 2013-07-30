__author__ = 'Orlowitz'

#TODO write to file then write to db
#TODO try except


import os, sys, re
import audit_log_2 as al
# import optparse
import shutil
import time



#command line stuff
# parser = optparse.OptionParser()
# parser.add_option('-d', help='audit file directory', dest='audit_dir')

# (opts, args) = parser.parse_args()

audit_dir = sys.argv[1] #opts.audit_dir #'./audit_files' #opts.audit_dir #'./audit_files' #directory of audit files
current_dir = os.getcwd()
files_to_process = os.listdir(audit_dir)
# print files_to_process



def process_dir(audit_dir):
    logins = {} #holder for records to write
    os.chdir(audit_dir)
    for file in files_to_process:
        if file != '.DS_Store':
            log_file = open(file, 'rb')
            log_f = log_file.read().split('\n')
            data = al.process_file(log_f)
            logins[file] = data
            log_file.close()
    os.chdir(current_dir)
    return logins

# l = process_dir(audit_dir)
# print l




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

def move_completed_files(files_to_move):
    os.chdir(audit_dir)
    files = files_to_move
    for file in files:
        if file != '.DS_Store':
            # shutil.move(file, os.path.join(current_dir, '/processed_audit_files'))
            shutil.move(file, current_dir + '/processed_audit_files/')
    os.chdir(current_dir)


def main():
    write_entries()
    print 'Done writing entries. Now moving files.'
    move_completed_files(files_to_process) #move files once processed.
    print 'Done processing audit files'


if __name__ == '__main__':
    main()



