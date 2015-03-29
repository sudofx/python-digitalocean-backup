#python-digitalocean-backup
##

######COMING SOON

python-digitalocean-backup is a python package that works with python-digitalocean to backup your droplets.

## How to install

    python setup.py install

```python
from digitaloceanbackup import *

token = "YOUR_TOKEN"
rsync_excludes = ["cache", "terminfo"]
remote_dirs    = ["/var/log", "/var/www"]

manager = digitalocean.Manager(token=token)
for droplet in manager.droplets:
    backup = Backup(
        droplet             = droplet,           #pass in a droplet obj
        ssh_user            = "root",            #ssh user
        ssh_key             = "droplet_ssh_key", #ssh key path/filename
        remote_dirs         = remote_dirs,       #remote folders to rsync
        rsync_excludes      = rsync_excludes,    #rsync excludes
        snapshot_hour       = 3,                 #hour of day to snapshot
        keep_snapshots      = 7                  #keep this many snapshots
    )

    print("backup finished")
    print(backup.success)
```