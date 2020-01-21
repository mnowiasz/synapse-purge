# synapse-purge
Purge old room events from your homeserver

This is basically the python version of  https://github.com/djmaze/synapse-purge,
which stopped working for me (after a ruby upgrade or two). I tried to fix it,
but since by ruby skills are non-existent I found it easier to reimplement the functionality
in python. It's also a nice exercise in python, especially in async/aio. 

## What it does
It fetches the list of rooms on your homeserver and sends - via the purge 
history API (https://github.com/matrix-org/synapse/blob/master/docs/admin_api/purge_history_api.rst)
purge requests, so old -by default remote- messages (for example, older than 120 days) 
are deleted. After that, it waits for the operation to finished.

Since this might be an expensive operation taking time, this is done asynchronously,
sending a number of parallel requests (by default 5) at the same time. Depending on your homeserver,
you might want to increase or decrease the number of workers.

You can do this on a daily basis, say by cron or systemd-timer, however, to
reclaim file system space you need to occasionally VACUUM FULL on the database

## Prerequisites
You need:
* access to synapse's database (postgresql only)
* an admin account on the homeserver
* Since the program uses the new API (_snapse/admin) you may have to configure
your reverse proxy to proxy _synapse requests to the homeserver


## Installation
* Clone the repository first. Depending on your preferences, you might want to create 
a virtual environment, use the (pre-)existing environment for the homeserver or
install it as user. So, either use
   * pip install --user . (user install) or
   * pip install . (virtual env)

After installation, you need to create a purge.conf. Take the supplied example.conf
as a template. You *must* change the entries that are not commented out. All 
other - commented in - entries are optional, if not set, the default values
(also documented in example.conf) are used.

   