## Synopsis:

This module works with [python-digitalocean](https://github.com/koalalorenzo/python-digitalocean) to allow you to rsync and snapshot your droplets with ease. **Great for hourly cron jobs!**

## How to install:

via pip

    pip install -U python-digitalocean-backup

via source

    python setup.py install


##### Example backup script (backup.py):

```python
import digitalocean
from digitaloceanbackup import backup

token = 'YOUR_TOKEN'
rsync_excludes = ['cache', '.DS_Store', 'man3', 'terminfo']
remote_dirs = ['/home', '/var/log', '/var/www']

manager = digitalocean.Manager(token=token)
for droplet in manager.get_all_droplets():
    backup(
        droplet=droplet,  # pass in a droplet obj
        ssh_user='droplet_ssh_user',  # ssh user
        ssh_key='droplet_ssh_key',  # ssh key file name or full path
        remote_dirs=remote_dirs,  # remote directories to rsync
        rsync_excludes=rsync_excludes,  # rsync excludes
        snapshot_hour=3,  # hour of day to take snapshot
        keep_snapshots=7  # keep this many snapshots
    )
```

##### Example hourly cron job:
```sh
0 * * * * /usr/bin/python /Users/username/bin/backup.py
```

###### Requires:
[python-digitalocean>=1.5](https://github.com/koalalorenzo/python-digitalocean)