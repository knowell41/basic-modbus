# basic-modbus

This project is aims to explore functionality of existing python modbus implementation [pymodbus](https://pymodbus.readthedocs.io/en/latest/index.html).

# [Demo](https://www.youtube.com/watch?v=SIxGnylKciE)
https://user-images.githubusercontent.com/45946492/233665072-9400698e-252a-4385-93af-19e86dd43dce.mp4


# Examples

## polling_example.py

Import modules

```
# polling_example.py

from basic_modbus.modbus_poll import ModbusPoll, ModbusPollError
import traceback
import time
```

Initialize modbus communication
```
server = ModbusPoll("COM8", scan_rate=0, timeout=0.5)
```

Add RTU
```
server.add_rtu(rtu_name="device_1", slave_id=1, address=0, quantity=4)
# server.add_rtu("device_2",2,0,4)
```
Start watching coil state
```
server.__enter__() # start polling rtu
```

Loop: Watch change in values in `server.rtu_readings`
```
# loop forever
# coil_state = False
prev = None        # initial value
while True:      
    try:
        current_readings = server.rtu_readings.copy()
        if prev != current_readings:
            print(current_readings)
            prev = current_readings.copy()

            ## do your logic here

    except (ModbusPollError, Exception) as e:
       server.__exit__() 
       break

```
## Write coil state

import `ModbusPoll`
```
from basic_modbus.modbus_poll import ModbusPoll
```
Initialize Modbus comminication

```
server = ModbusPoll("COM8", scan_rate=0, timeout=0.5)
```

Send command to target RTU
```
server.write_coil(
    address=0, # coil address
    value=True, # coil state True=On | False=Off
    slave_id=1 # RTU slave address
)
```
