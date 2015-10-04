## Synopsis:

This module works with [python-digitalocean](https://github.com/koalalorenzo/python-digitalocean) to allow you to rsync and snapshot your droplets with ease. **Great for hourly cron jobs!**

###### Works with posix (*nix, osx, cygwin)
Tested with Python 2.7.8(CYGWIN), 2.7.9(OS X/Linux), 3.4.3(OS X/Linux)


## How to install:

[PyPI package](https://pypi.python.org/pypi/python-digitalocean-backup)

via pip

    pip install -U python-digitalocean-backup

via source

    python setup.py install

##  

##### *NEW*: Requires a config file to store your token in $HOME/.digitalocean

```bash
[digitalocean]
token = YOUR_DIGITALOCEAN_TOKEN
```

##### Example backup script (backup.py):

```python
from digitaloceanbackup import *

for droplet in DigitalOcean().droplets:
    Backup(
        droplet=droplet,
        ssh_user="root",
        ssh_key="do_rsa",
        remote_dirs=['/home', '/var/log', '/var/www'],
        rsync_excludes=['cache', '.DS_Store', 'man3'],
        snapshot_hour=2,
        keep_snapshots=7,
        debug=False
    )

```

##### Example hourly cron job:
```sh
0 * * * * /usr/bin/python /Users/username/bin/backup.py
```

###### Requires:
[python-digitalocean>=1.5](https://github.com/koalalorenzo/python-digitalocean)
