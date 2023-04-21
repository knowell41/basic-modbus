# basic-modbus

This project is aims to explore functionality of existing python modbus implementation [pymodbus](https://pymodbus.readthedocs.io/en/latest/index.html).

# Demo



https://user-images.githubusercontent.com/45946492/233665072-9400698e-252a-4385-93af-19e86dd43dce.mp4



# Sample code
```
# polling_example.py

from basic_modbus.modbus_poll import ModbusPoll, ModbusPollError
import traceback
import time

"""
Sends modbus request to read coils of each RTU,
"""


server = ModbusPoll("COM8", scan_rate=0, timeout=0.5)
server.add_rtu("device_1", 1, 0, 4)
# server.add_rtu("device_2",2,0,4)

server.__enter__() # start pollin rtu
prev = None        # initial value

# loop forever
# coil_state = False
while True:      
    try:
        current_readings = server.rtu_readings.copy()
        if prev != current_readings:
            print(current_readings)
            prev = current_readings.copy()

        # wacth for failed modbus poll
        # if server.error:
        #     print(server.error)
        #     server.error = None

        # blocking function to write state to coil
        # server.write_coil(address=0, value=coil_state, slave_id=1)

        # invert coil_state to make it blink
        # coil_state = not coil_state

    except (ModbusPollError, Exception) as e:
       server.__exit__() 
       break


```
