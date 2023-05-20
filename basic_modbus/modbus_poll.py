

import serial
import time
import traceback
from pymodbus.client.mixin import ModbusClientMixin
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusException, NoSuchSlaveException, ModbusIOException
import time
import threading
import logging
from typing import Any, List, Tuple, Union


WRITE_SINGLE_COIL = 5
WRITE_SINGLE_REGISTER = 6
WRITE_COILS = 15
WRITE_REGISTERS = 16
REPORT_SERVER_ID = 17
READ_COILS = 1

class ModbusPollError(Exception):
    pass

class ModbusPoll:
    def __init__(self, port:str, baudrate:int=9600, timeout:float=0.5, scan_rate:float=0.5):
        """**ModbusPoll**
        :param port: Serial port used for communication.
        :param baudrate: (optional) Bits per second.
        :param timeout: (optional) serial timeout.
        :param scan_rate: (optional) polling delay.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.scan_rate = scan_rate

        
        self.rtu = []
        self.rtu_readings = []
        self.running = False
        self.client = ModbusSerialClient(self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.write_to_coil = None
        self.write_multiple_coil_value = None
        self.error = None

    def disconnect_serial(self):
        """**disconnecT_serial**
        Disconnect to serial.
        """
        if self.client.connected:
            self.client.close()

    def connect_serial(self):
        """**connect_serial**
        Connect to serial.
        """
        if not self.client.connected:
            self.client.connect()

    def add_rtu(self, rtu_name:str, slave_id:int, address:int, quantity:int):
        """**add_rtu**
        Adds RTU to poll.
        :param rtu_name: Name of the RTU.
        :param slave_id: Slave ID.
        :param address: Coil start address.
        :param quantity: number of coils.
        """
        for dev in self.rtu:
            if dev.get("slave_id") == slave_id:
                return False, f"Unable to add RTU with slave_id {slave_id}."
            
        self.rtu.append({
            "name": rtu_name,
            "slave_id": slave_id,
            "address": address,
            "quantity": quantity
        })
        return True, f"RTU with slave_id {slave_id} added successfully."
    
    def write_coil(self, address:int, value:bool, slave_id:int)->None:
        """**write_coil**
        Blocking function to write coil state
        """
        self.write_to_coil = (address, value, slave_id)
        while self.write_to_coil != None:
            pass

    def write_multiple_coils(self,
        address: int,
        values: Union[List[bool], bool],
        slave: int = 0)->None:
        """Write coils (code 0x0F).

        :param address: Start address to write to
        :param values: List of booleans to write, or a single boolean to write
        :param slave: (optional) Modbus slave ID
        :param kwargs: (optional) Experimental parameters.
        :raises ModbusException:
        """

        self.write_multiple_coil_value = (address, values, slave)

        while self.write_multiple_coil_value != None:
            pass
        

    def poll(self):
        """**poll**
        Polling registered rtu with frequency defined by scan_rate
        """

        self.connect_serial()
        cmd = dict()
        for rtu in self.rtu:
            cmd[rtu["name"]] = (rtu["address"], rtu["quantity"], rtu["slave_id"])
        last_readings = []
        while self.running:
            response = {}
            for key in cmd.keys():
                try:
                    last_readings =  self.client.read_coils(cmd[key][0], cmd[key][1],cmd[key][2] ).bits
                    response[key] = last_readings
                    self.error = None
                except Exception as e:
                    response[key] = last_readings
                    self.error = e
                    
                    
            self.rtu_readings = response.copy()
            if self.write_to_coil:
                self.client.write_coil(self.write_to_coil[0], self.write_to_coil[1], self.write_to_coil[2])
                self.write_to_coil = None
            elif self.write_multiple_coil_value:
                self.client.write_coils(self.write_multiple_coil_value[0], self.write_multiple_coil_value[1], self.write_multiple_coil_value[2])
                self.write_multiple_coil_value = None

            time.sleep(self.scan_rate)

    def __enter__(self):
        """
        start polling
        """
        if not self.running:
            self.running = True
            self.poll_thread = threading.Thread(target=self.poll, daemon=True)
            self.poll_thread.start()
            print("modbus poll started")
        else:
            print("modbus poll is already running")

    def __exit__(self):
        """
        end polling
        """
        if self.running:
            self.running = False
            self.poll_thread.join()
            self.rtu_readings = dict()
            self.disconnect_serial()
            print("modbus poll stop")
        else:
            print("modbus poll is not running.")
