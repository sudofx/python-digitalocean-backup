"""Tested with Python 2.7 & Python 3.4"""
import os
import sys
import time
import datetime
import getpass
import shlex
import subprocess

"""Backup your Digitalocean Droplets"""
__version__ = "1.0"
__author__ = "Rob Johnson ( http://corndogcomputers.com )"
__author_email__ = "info@corndogcomputers.com"
__license__ = "The MIT License (MIT)"
__copyright__ = "Copyright (c) 2015 Rob Johnson"


class Backup(object):

    """"
    Attributes accepted at creation time:
        droplet: Droplet - droplet obj
        ssh_user: str - user for rsync connections when connecting to droplet
        ssh_key: str - ssh key file (full path/key_name) NO PASSWORD ACCESS
        remote_dirs: [str] - list of directories to rsync from droplet to local
        rsync_excludes: [str] - list of  rsync excludes
        snapshot_hour: int - the hour of day to create a snapshot
        keep_snapshots: int - number of backup snapshots to keep
        backup_dir: str - the local folder for your droplet backups
        delay: int - api delay between calls
    """

    def __init__(self, *args, **kwargs):
        self.success = None
        self.delay = 5
        self.ssh_user = ""
        self.ssh_key = ""
        self.remote_dirs = []
        self.rsync_excludes = []
        self.freshlog = False
        self.use_ip = False
        self.user = getpass.getuser()
        self.home = os.path.expanduser("~")
        self.backup_dir = "%s/Droplets" % self.home
        self.snapshot_hour = 25
        self.keep_snapshots = 0

        """Currently no support for Windows."""
        if os.name != "posix":
            sys.exit("Currently only supports POSIX OS.")

        """Set attributes from args."""
        self.__dict__.update(kwargs)

        """Let's check to make sure a droplet was passed in."""
        if hasattr(self, "droplet") == True:
            """Set the prefered route (ip or droplet name)."""
            self.route = self.droplet.name
            if self.use_ip == True:
                self.route = droplet.ip_address

            """Clear the logfile and start over if this is a snapshot_hour."""
            self.freshlog = (
                datetime.datetime.today().hour == self.snapshot_hour)

            """Set the default backup_dir to $HOME/Droplets/droplet.name."""
            if self.droplet.name not in self.backup_dir:
                self.backup_dir = "%s/%s" % (
                    self.backup_dir, self.droplet.name)

            """Create the backup_dir if it doesn't exist."""
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)

            """Try to get and set the full ssh key path."""
            self.ssh_key = self.__find_ssh_key()

            """Set the log file name."""
            self.logfile = "%s/%s" % (self.backup_dir, "_backup_log.md")
            self.success = self.__rsync()
        else:
            sys.exit("No droplet specified for backup...\n")

    """Add entry to self.logfile."""

    def __log(self, msg):
        timestamp = "#####[%s]" % (
            str(datetime.datetime.fromtimestamp(
                int(time.time())).strftime("%Y-%m-%d-%H%M")
                )
        )
        msg = "%s %s\n" % (timestamp, msg)

        """Write to self.logfile."""
        if self.freshlog == True:
            logfile = open(self.logfile, 'w')
            self.freshlog = False
        else:
            logfile = open(self.logfile, 'a')

        logfile.writelines(msg)
        logfile.close()

    """Try to loacate and return the full ssh_key path."""

    def __find_ssh_key(self):
        this_path = "%s/%s" % (os.getcwd(), self.ssh_key)
        home_path = "%s/%s" % (self.home, self.ssh_key)
        ssh_path = "%s/.ssh/%s" % (self.home, self.ssh_key)
        paths = [self.ssh_key, this_path, home_path, ssh_path]
        for path in paths:
            if os.path.isfile(path):
                return path
        sys.ext("could not find ssh_key: %s" % self.ssh_key)

    """Checks for ssh and rsync."""

    def __bin_checks(self):
        found = False
        missing_bin = ""
        for bin_name in ["ssh", "rsync"]:
            for path in os.environ["PATH"].split(os.pathsep):
                found = False
                bin_path = os.path.join(path.strip('"'), bin_name)
                if os.path.isfile(bin_path) and os.access(bin_path, os.X_OK):
                    found = True
                    break
                else:
                    missing_bin = bin_path
        return found if (found == True) else sys.exit("%s not found" % missing_bin)

    """Check for remote directories."""

    def __remote_dir_check(self, remote_dir):
        result = False
        ssh_cmd = "ssh -oStrictHostKeyChecking=no -i %s" % self.ssh_key
        local_dir = "%s%s/" % (self.backup_dir, remote_dir)

        """
            If the local_dir doesn't exist, let's ssh into the server and check
            if the remote_dir exists on the server. If it does, then we'll
            create the local_dir and then we won't need to check for it again.
        """
        process = "%s %s@%s [ -d %s ] && echo True || echo False" % (
            ssh_cmd, self.ssh_user, self.route, remote_dir
        )

        """Create the local_dir for the remote_dir if it doesn't exits."""
        if not os.path.exists(local_dir):
            output = self.__run_process(process)
            if "True" in output:
                """Create the local_dir if it doesn't exits."""
                os.makedirs(local_dir)
                self.__log("CREATING_LOCAL_DIRECTORY: _%s_" % local_dir)
                result = True
            else:
                self.__log("DROPLET_DIRECTORY_NOT_EXIST: _%s_" % remote_dir)
                result = False
        else:
            result = True

        return result

    """Run shell commands on droplet."""

    def __run_process(self, process):
        try:
            output = subprocess.Popen(
                shlex.split(process),
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                universal_newlines=True,
                shell=False
            ).communicate()[0]
        except subprocess.CalledProcessError as grepexc:
            status = grepexc.returncode
            output = grepexc.output
            print(status, output)
        return output

    """This will delete old snapshots created by this backup."""

    def __delete_snapshots(self):
        complete = False
        snapshots = []
        self.droplet.load()

        droplet_snapshots = self.droplet.get_snapshots()

        if len(droplet_snapshots):
            for snapshot in droplet_snapshots:
                snapshot.load()
                if ("@%s-" % self.droplet.name) in snapshot.name:
                    snapshots.append(snapshot)

            count = len(snapshots)

            if count > 0:
                while count > self.keep_snapshots:
                    complete = False
                    snapshot = snapshots[0].load()
                    complete = snapshot.destroy()
                    snapshots.pop(0)
                    count = len(snapshots)

                    """Log the snapshot name and complete result."""
                    self.__log("DROPLET_SNAPSHOT_DELETE: _%s_ %s" % (
                        snapshot.name, complete))
            else:
                complete = True
        else:
            complete = True

        return complete

    """This will power off the droplet and take a snapshot."""

    def __take_snapshot(self):
        complete = False

        """Is it time to take a snapshot?"""
        if (datetime.datetime.today().hour == self.snapshot_hour):
            timestamp = str(datetime.datetime.fromtimestamp(
                int(time.time())).strftime('%Y-%m-%d-%H%M'))

            """Create a snapshot with a name like @example.com-2015-29-0300."""
            snapshot_name = "@%s-%s" % (self.droplet.name, timestamp)

            off = self.droplet.status == "off"
            if off == False:
                off = self.droplet.power_off(return_dict=False).wait(
                    update_every_seconds=self.delay)

            if off == True:
                """Take the snapshot."""
                complete = self.droplet.take_snapshot(
                    snapshot_name,
                    return_dict=False
                ).wait(update_every_seconds=(self.delay * 2))

                """Log the snapshot name and complete result."""
                self.__log("DROPLET_TAKING_SNAPSHOT: _%s_ %s" % (
                    snapshot_name, complete))

                if self.keep_snapshots != 0:
                    complete = self.__delete_snapshots()
        else:
            complete = True

        return complete

    """The main rsync function."""

    def __rsync(self):
        """Log the Python version."""
        self.__log("PYTHON_VERSION: _%s_" % sys.version.split()[0])

        """Log the connection route."""
        self.__log("DROPLET_CONNECTION_ROUTE: _%s_" % self.route)

        complete = False
        if len(self.remote_dirs):
            """Check the droplet status and power it on if not 'active'."""
            if (self.droplet.status != "active"):
                self.droplet.power_on(return_dict=False).wait(
                    update_every_seconds=self.delay)

            if self.__bin_checks():
                rsync = "rsync -avz --update"
                excludes = ""

                for exclude in self.rsync_excludes:
                    excludes = "%s--exclude '%s' " % (excludes, exclude)

                for remote_dir in self.remote_dirs:
                    if self.__remote_dir_check(remote_dir) == True:
                        complete = False
                        params = "-e 'ssh -oStrictHostKeyChecking=no -i %s'" % self.ssh_key
                        """This is the actual rsync command being sent."""
                        process = "%s %s %s %s@%s:%s/ %s%s" % (rsync, excludes,
                                                               params, self.ssh_user, self.droplet.name, remote_dir,
                                                               self.backup_dir, remote_dir
                                                               )

                        output = self.__run_process(process)

                        """Format the output for markdown."""
                        output = "%s\n" % output
                        output = output.replace("\nsent", "sent")
                        output = output.replace(" \n", "\n")
                        output = output.replace(
                            "receiving file list ... done", "")
                        output = output.replace("\n", "\n* ")
                        output = output.replace("\n* \n", " ")
                        output = output.replace(" * ", "")

                        """Log the markdown output."""
                        self.__log("_syncing %s..._ %s\n" %
                                   (remote_dir, output))
                        complete = True
                    else:
                        complete = True
        else:
            complete = True

        if self.snapshot_hour != 25:
            complete = self.__take_snapshot()

        self.__log("DROPLET_BACKUP_FINISHED")
        self.__log(
            "**====================================================**\n\n")

        return complete
