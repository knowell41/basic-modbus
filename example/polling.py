from basic_modbus.modbus_poll import ModbusPoll
import traceback
import time

server = ModbusPoll("COM8", scan_rate=0.3, timeout=0.5)
server.add_rtu("device_1", 1, 0, 4)
# server.add_rtu("device_2",2,0,4)


server.__enter__()
prev = None
bval = True
while True:
    try:
        current_readings = server.rtu_readings.copy()
        if prev != current_readings:
            print(current_readings)
            prev = current_readings.copy()

        bval = not bval
        # (relay #, True/False, slave_id)
        server.write_to_coil = (0, bval, 1)
        while not server.write_to_coil:
            pass
        
    except:
       print(f"ERROR: {traceback.format_exc()}")
       server.__exit__() 
       break
