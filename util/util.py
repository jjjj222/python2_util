import os
from cStringIO import StringIO

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def get_real_path(path):
    path = os.path.expanduser(path);
    path = os.path.realpath(path)
    return path

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#   tokenize
#-------------------------------------------------------------------------------
# TODO: support double quote (")
def tokenize_tcl_list(tcl_list):

    iter = enumerate(tcl_list)

    result = tokenize_tcl_list_helper(iter)

    return result


def tokenize_tcl_list_helper(iterator):
    result = []
    try:
        sstm = StringIO()
        while True:
            i, c = next(iterator)
            if c == "{":
                nested_result = tokenize_tcl_list_helper(iterator)
                result.append(nested_result)
            elif c == "}":
                break
            elif c == " ":
                token = sstm.getvalue()
                sstm = StringIO()
                if len(token) != 0:
                    result.append(token)
            else:
                sstm.write(c)

    except StopIteration:
        pass

    token = sstm.getvalue()
    sstm = StringIO()
    if len(token) != 0:
        result.append(token)

    return result

#-------------------------------------------------------------------------------
#   assert
#-------------------------------------------------------------------------------
def assert_and_get_env(name):
    value = os.environ.get(name);
    if value == None:
        raise SystemExit("Error: No environment variable '%s' !!" % name)
    return value

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def dump_dict(d):
    print "{"
    for key, value in d.iteritems():
        print "    \"%s\": \"%s\"," % (key, value)
    print "}"
