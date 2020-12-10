# led-manager

## setup

### systemd

Edit the file `systemd-service/led-manager.service` filling in the
path to where this git repository is checked out, and the name of the
user who checked out the repository.

The script will be run as that user rather than as root.

```
cp systemd-service/led-manager.service /etc/systemd/system/led-manager.service
```