# led-manager

## setup

### systemd

Edit the file `systemd-service/led-manager.service` filling in the
path to where this git repository is checked out, and the name of the
user who checked out the repository.

The script will be run as that user rather than as root.

```
cp systemd-service/led-manager.service /etc/systemd/system/
```

### web interface

This was setup assuming the default raspberrypi OS install, using
lighttpd as a web server.  The cgi module needs to be enabled.  All
the configuration files were left otherwise unaltered.

Then:

```
cp www/html/index.html /var/www/html/
cp www/html/spinner.gif /var/www/html/
cp www/cgi-bin/led-manager.py /usr/lib/cgi-bin/
```
