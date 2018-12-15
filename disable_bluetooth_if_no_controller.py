import threading
import time
import os
import glob

TIME_OUT = 60 * 5

last_time_controller_used = None
power_button_timer = 0
registered_devices = set()

def check_for_input(input_device):
    global last_time_controller_used, power_button_timer
    print('Registered %s' % input_device)
    try:
        with open(input_device, "rb" ) as rb:
            while True:
                data = rb.read(8)
                last_time_controller_used = time.time()
    except OSError:
        registered_devices.remove(input_device)
        print('Device %s unregistered.' % input_device)



print(
    'This script scans for Bluetooth controllers and '
    'disconnects all Bluetooth devices if there are no '
    'activity in %i seconds' % TIME_OUT
)
i = 0
while True:
    for input_device in glob.glob('/dev/input/js*'):
        if input_device not in registered_devices:
            registered_devices.add(input_device)
            threading.Thread(target=lambda: check_for_input(input_device)).start()

    if i == 0 and len(registered_devices) == 0:
        print('Warning: There are no connected Bluetooth controllers...')

    if len(registered_devices) > 0 and last_time_controller_used:
        time_diff = time.time() - last_time_controller_used
        if time_diff >= TIME_OUT:
            print('Controllers have not been used in %i seconds' % TIME_OUT)
            print('Shutting down Bluetooth temporarily...')
            os.system('sudo service bluetooth stop')
            os.system('sudo service bluetooth start')
            last_time_controller_used = time.time()
        #print('Controller was last used in %i seconds' % time_diff)
    time.sleep(1)
    i += 1
