import sys
import os
import subprocess
import re
from cStringIO import StringIO

#-------------------------------------------------------------------------------
#   p4python
#-------------------------------------------------------------------------------
P4PYTHON_LIB_PATH = '/home/utils/p4python-2014.1.925900/lib/'
sys.path.insert(1, P4PYTHON_LIB_PATH)
from P4 import P4, P4Exception

#-------------------------------------------------------------------------------
#   my lib
#-------------------------------------------------------------------------------
import util.cmd as cmd_util
import util.file as file_util

#-------------------------------------------------------------------------------
#   Is
#-------------------------------------------------------------------------------

def is_valid_client_name(name):
    p4 = P4()
    try:
        p4.connect()
        p4.fetch_client(name)
    except P4Exception:
        return False

    return True

def is_client_exist(name):
    if not is_valid_client_name(name):
        return False

    cmd = "p4 -ztag -F %Update% client -o"
    output = subprocess.check_output(cmd.split() + [name]).strip()
    return output != ""

def is_client_uptodate(client_name):
    assert_client_exist(client_name)
    sstm = StringIO()

    cmd = "p4 -c " + client_name + " sync -n"
    cmd_util.run_cmd_no_progress(sstm, cmd)
    #print sstm.getvalue()
    return sstm.getvalue().strip() == "File(s) up-to-date."

def is_standard_client_name(name):
    pattern = re.compile("^nvtools_[0-9]+_.+$")
    return re.match(pattern, name)

#-------------------------------------------------------------------------------
#   Assert
#-------------------------------------------------------------------------------
def assert_client_not_exist(name):
    if is_client_exist(name):
        raise AssertionError("Client '%s' has existed" % name)

def assert_client_exist(name):
    if not is_client_exist(name):
        raise AssertionError("Client '%s' doesn't exist" % name)

def assert_valid_client_name(name):
    if not is_valid_client_name(name):
        raise ValueError("'%s' is not a valid client name" % name)

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def get_client_root(client_name):
    if not is_client_exist(client_name):
        return None

    result = None
    p4 = P4()
    try:
        p4.connect()
        client = p4.fetch_client(client_name)
        result = client["Root"]

    except P4Exception:
        for e in p4.errors:
            print e

    return result

def get_client_spec(client_name):
    p4 = P4()
    p4.connect()
    return p4.fetch_client(client_name)


#-------------------------------------------------------------------------------
#   print
#-------------------------------------------------------------------------------
def print_p4config(ostream, client_name):
    ostream.write("P4CLIENT=%s" % client_name)

#-------------------------------------------------------------------------------
#   Create
#-------------------------------------------------------------------------------
def create_p4config(client_root, client_name):
    file_util.assert_isdir(client_root)

    filename = os.path.join(client_root, ".p4config");
    file_util.assert_not_exist(filename)

    with open(filename, 'w') as p4config:
        print_p4config(p4config, client_name)
        p4config.close()

#-------------------------------------------------------------------------------
def create_client_spec_file(client_root, client, filename):
    file_util.assert_isdir(client_root)
    file_util.assert_not_exist(filename)

    with open(filename, 'w') as spec_file:
        print_client_spec(spec_file, client_root, client)

#-------------------------------------------------------------------------------
def create_client_from_spec(client_spec):
    p4 = P4()
    try:
        p4.connect()
        p4.save_client(client_spec)
    except P4Exception:
        for e in p4.errors:
            print e

#-------------------------------------------------------------------------------
def sync_client(client_name, logfile=None):
    assert_client_exist(client_name)
    if logfile:
        ostream = logfile
    else:
        ostream = sys.stdout

    cmd = "p4 -c " + client_name + " sync"
    cmd_util.run_cmd(ostream, cmd)

#-------------------------------------------------------------------------------
#   Remove
#-------------------------------------------------------------------------------
def remove_client(client_name):
    assert_client_exist(client_name)
    #p4 = P4()
    #p4.connect()
    #p4.delete_client(client_name)
    cmd = "p4 client -d " + client_name
    ostream = sys.stdout
    cmd_util.run_cmd_oneline(ostream, cmd)

#-------------------------------------------------------------------------------
def main():
    pass

#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
