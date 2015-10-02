#!/usr/bin/env python

from digitaloceanbackup import *

rsync_excludes = [
    "wpcf7_captcha",
    "cache",
    ".DS_Store",
    "man3",
    "terminfo"
]

remote_dirs = [
    "/root",
    "/home",
    "/etc",
    "/usr/local",
    "/usr/share",
    "/usr/bin",
    "/usr/sbin",
    "/var/backups",
    "/var/mail",
    "/var/log",
    "/var/www"
]

for droplet in DigitalOcean().droplets:
    Backup(
        droplet=droplet,
        ssh_user="root",
        ssh_key="do_rsa",
        remote_dirs=remote_dirs,
        rsync_excludes=rsync_excludes,
        snapshot_hour=2,
        keep_snapshots=7,
        debug=False
    )
