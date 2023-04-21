# polling_example.py

from basic_modbus.modbus_poll import ModbusPoll, ModbusPollError
import traceback
import time

"""
Sends modbus request to read coils of each RTU,
"""


server = ModbusPoll("COM8", scan_rate=0, timeout=0.5)
server.add_rtu(rtu_name="device_1", slave_id=1, address=0, quantity=4)
# server.add_rtu("device_2",2,0,4)

server.__enter__() # start polling rtu

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
