# polling_example.py

from basic_modbus.modbus_poll import ModbusPoll, ModbusPollError


"""
Sends modbus request to turn on|off coils.
"""


server = ModbusPoll("COM8", scan_rate=0, timeout=0.5)

server.write_coil(
    address=0, # coil address
    value=True, # coil state True=On | False=Off
    slave_id=1 # RTU slave address
)