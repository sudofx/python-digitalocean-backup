# python-digitalocean-backup

Python module that works with python-digitalocean to manage droplet backups.

##### Requires:
[python-digitalocean>=1.5](https://github.com/koalalorenzo/python-digitalocean)

##### How to install:

via pip

    pip install -U python-digitalocean-backup

via source

    python setup.py install


##### Example:

```python
import digitalocean
from digitaloceanbackup import Backup

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


# Example Log: [markdown]

#####[2015-04-01-0927] PYTHON_VERSION: _3.4.3_
#####[2015-04-01-0927] DROPLET_CONNECTION_ROUTE: _svr.example.com_
#####[2015-04-01-0927] _syncing /home..._ 
* sent 85 bytes  received 1269795 bytes  282195.56 bytes/sec
* total size is 2891288481  speedup is 2276.82

#####[2015-04-01-0928] _syncing /var/log..._ 
* auth.log
* nginx/access.log
* upstart/systemd-logind.log
* sent 20557 bytes  received 8123 bytes  11472.00 bytes/sec
* total size is 122684370  speedup is 4277.70

#####[2015-04-01-0928] _syncing /var/www..._ 
* sent 85 bytes  received 1525 bytes  1073.33 bytes/sec
* total size is 1025218  speedup is 636.78

#####[2015-04-01-0928] DROPLET_BACKUP_FINISHED
#####[2015-04-01-0928] **====================================================**


