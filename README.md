#python-digitalocean-backup

python-digitalocean-backup is a python module that works with python-digitalocean to manage droplet backups.

##### How to install

    python setup.py install

##### Example script

```python
import digitalocean
import digitaloceanbackup

token = "YOUR_TOKEN"

rsync_excludes = ["cache", ".DS_Store", "man3", "terminfo"]
remote_dirs = ["/root", "/home", "/etc", "/usr/local", "/usr/share",
               "/var/backups", "/var/mail", "/var/log", "/var/www"]

manager = digitalocean.Manager(token=token)
for droplet in manager.droplets:
    backup = digitaloceanbackup.Backup(
        droplet=droplet,  # pass in a droplet obj
        ssh_user="root",  # ssh user
        ssh_key="your_ssh_key",  # ssh key file name or full path
        remote_dirs=remote_dirs,  # remote directories to rsync
        rsync_excludes=rsync_excludes,  # rsync excludes
        snapshot_hour=3,  # hour of day to take snapshot
        keep_snapshots=7  # keep this many snapshots
    )
```