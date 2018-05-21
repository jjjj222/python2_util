import os
import subprocess

import time_util

#-------------------------------------------------------------------------------
#   
#-------------------------------------------------------------------------------
def run_cmd(ostream, cmd, cwd=None, env=None, with_timestamp=False, show_env=[]):
    print_progress(ostream, cmd, "START", cwd)
    if env:
        print_env(ostream, show_env, env)
    else:
        print_env(ostream, show_env)

    proc = subprocess.Popen(cmd.split(), cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(proc.stdout.readline,''):
        if with_timestamp:
            ostream.write(time_util.timestamp())
            ostream.write(" - ")
        ostream.write(line.rstrip())
        ostream.write("\n")
        ostream.flush()

    print_progress(ostream, cmd, "END", cwd)

def run_cmd_oneline(ostream, cmd, cwd=None, env=None, show_env=[]):
    print_progress(ostream, cmd, "CMD", cwd)
    if env:
        print_env(ostream, show_env, env)
    else:
        print_env(ostream, show_env)

    proc = subprocess.Popen(cmd.split(), cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(proc.stdout.readline,''):
        ostream.write(line.rstrip())
        ostream.write("\n")
        ostream.flush()

def run_cmd_no_progress(ostream, cmd, cwd=None, env=None):
    proc = subprocess.Popen(cmd.split(), cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(proc.stdout.readline,''):
        ostream.write(line.rstrip())
        ostream.write("\n")
        ostream.flush()

#-------------------------------------------------------------------------------
def print_progress(ostream, cmd, status, dir):
    ostream.write(time_util.timestamp())
    ostream.write(" - (%s) " % status)
    ostream.write(cmd)
    if dir:
        ostream.write(" (in ")
        ostream.write(dir)
        ostream.write(")")
    ostream.write("\n")
    ostream.flush()

def print_env(ostream, env_names, env=None):
    if not env:
        env = os.environ

    for e in env_names:
        value = env.get(e)
        if value == None:
            value = "<UNDEFINED>"
        ostream.write("%s = %s\n" % (e, value))
        ostream.flush()
