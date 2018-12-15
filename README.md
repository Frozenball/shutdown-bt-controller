# shutdown-bt-controller
Shutdowns Bluetooth controllers if they are not used in N minutes. This works at least with DS4.

## Installation

````
$ sudo crontab -e
```` 

and put this:

````
@reboot python3 /home/user/disable_bluetooth_if_no_controller.py > /var/log/bluetooth.log
````
