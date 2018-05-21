import os
import errno

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def assert_exist(filename):
    if not os.path.exists(filename):
        raise SystemExit("'%s' doesn't exist !!" % filename)

def assert_not_exist(filename):
    if os.path.exists(filename):
        raise SystemExit("'%s' already exist !!" % filename)

def assert_isdir(dirname):
    if not os.path.isdir(dirname):
        raise AssertionError("'%s' is not a directory !!" % dirname)

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def createDir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise SystemExit("Error: can't create directory %s !!" % path)

#-------------------------------------------------------------------------------
def removeFile(filename):
    try:
        os.remove(filename)
    except OSError:
        pass
