import os
import sys

# my lib
import util.util as util
import util.cmd as cmd_util
import util.file as file_util

#-------------------------------------------------------------------------------
#   Bullseye
#-------------------------------------------------------------------------------
class Bullseye:
    """Control Bullseye"""

    def __init__(self, build_zone):
        self.build_zone = build_zone
        self.cov_file = os.path.join(self.build_zone, "bullseye.cov")
        #self.region_file = self.cov_file + ".region"
        #self.region_file = None
        self.html_folder = self.cov_file + ".html"
        self.csv_file = self.cov_file + ".csv"
        self.bullshtml_folder = self.cov_file + ".bullshtml"

        self.bin = None
        self.bullshtml_jar = None

    @property
    def cov01(self):
        return os.path.join(self.bin, "cov01")

    @property
    def covselect(self):
        return os.path.join(self.bin, "covselect")

    @property
    def covhtml(self):
        return os.path.join(self.bin, "covhtml")

    @property
    def covsrc(self):
        return os.path.join(self.bin, "covsrc")

    @property
    def covxml(self):
        return os.path.join(self.bin, "covxml")

    def on(self):
        cmd = self.cov01 + " --on"
        env = os.environ.copy()
        env["COVFILE"] = self.cov_file
        env["COVBUILDZONE"] = self.build_zone
        show_env = ["COVFILE", "COVBUILDZONE"]

        ostream = sys.stdout
        cmd_util.run_cmd_oneline(ostream, cmd, None, env, show_env)

    def off(self):
        cmd = self.cov01 + " --off"
        env = os.environ.copy()
        env["COVFILE"] = self.cov_file
        env["COVBUILDZONE"] = self.build_zone
        show_env = ["COVFILE", "COVBUILDZONE"]

        ostream = sys.stdout
        cmd_util.run_cmd_oneline(ostream, cmd, None, env, show_env)

    def apply_region(self, region_file):
        if not region_file:
            return

        #cmd = self.covselect + " --file " + self.cov_file + " --import " + self.region_file
        cmd = self.covselect + " --file " + self.cov_file + " --import " + region_file

        show_env = []

        ostream = sys.stdout
        cmd_util.run_cmd_oneline(ostream, cmd, None, None, show_env)

    def generate_html(self):
        cmd = self.covhtml + " --file " + self.cov_file + " " + self.html_folder

        show_env = []

        ostream = sys.stdout
        cmd_util.run_cmd_oneline(ostream, cmd, None, None, show_env)

    def generate_csv(self):
        cmd = self.covsrc + " --file " + self.cov_file + " --csv --quiet"
        cwd = self.build_zone

        show_env = []

        print "Create bullseye result csv file:", self.csv_file
        ostream = open(self.csv_file, 'w')
        cmd_util.run_cmd_no_progress(ostream, cmd=cmd, cwd=cwd)

    def generate_bullshtml(self):
        cmd = "java -jar " + self.bullshtml_jar + " -f " + self.cov_file + " -s " + self.build_zone + " -c " + self.covxml + " " + self.bullshtml_folder

        show_env = []

        ostream = sys.stdout
        cmd_util.run_cmd_oneline(ostream, cmd, None, None, show_env)

    #def remove_cov_file(self):
    #    file_util.removeFile(self.cov_file)
