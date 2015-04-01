#python-digitalocean-backup

python-digitalocean-backup is a python module that works with python-digitalocean to manage droplet backups.

##### Requires:
[python-digitalocean>=1.5](https://github.com/koalalorenzo/python-digitalocean)
(currently not on PyPi)

##### How to install:

    python setup.py install

##### Example:

```python
import digitalocean
import digitaloceanbackup

token = "YOUR_TOKEN"
rsync_excludes = ["cache", ".DS_Store", "man3", "terminfo"]
remote_dirs = ["/home", "/var/log", "/var/www"]

manager = digitalocean.Manager(token=token)
for droplet in manager.get_all_droplets():
    Backup(
        droplet=droplet,  # pass in a droplet obj
        ssh_user="droplet_ssh_user",  # ssh user
        ssh_key="droplet_ssh_key",  # ssh key file name or full path
        remote_dirs=remote_dirs,  # remote directories to rsync
        rsync_excludes=rsync_excludes,  # rsync excludes
        snapshot_hour=3,  # hour of day to take snapshot
        keep_snapshots=7  # keep this many snapshots
    )
```