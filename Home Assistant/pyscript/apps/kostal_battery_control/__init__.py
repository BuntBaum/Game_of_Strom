from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder



@time_trigger("period(0:00, 5 sec)") # This will trigger every 5 seconds
def kostal_battery_control():
    log.info("Hallo Battery Control")

    # Available via Kostal Integration (via REST-API)
    # https://www.home-assistant.io/integrations/kostal_plenticore/
    
    home_power_from_grid = int(sensor.scb_home_power_from_grid) 
    grid_power = int(sensor.scb_grid_power)
    battery_power = int(sensor.scb_battery_power)
    battery_soc = int(sensor.scb_battery_soc)
    battery_soc_min = int(number.scb_battery_min_soc)

    # Could be made available via Kostal Modbus
    max_discharge_power_1040 = 2750
    max_charge_power_1038 = -2750
    battery_soc_max_1044 = 95


    new_battery_power = 0 # Set default value

    if battery_soc < battery_soc_min: # If Battery should be charged --> CHARGE battery more
        new_battery_power = max_charge_power_1038


    if home_power_from_grid > 0: # If Power is taken from the grid for home consumption --> Try to DISCHARGE the battery more
        if battery_soc > battery_soc_min: # If Battery not empty
            new_discharge_power = battery_power # reuse any existing discharge power            
            new_discharge_power = max(new_discharge_power, 0) # avoid negative values that would charge the battery
            new_discharge_power = new_discharge_power + ((home_power_from_grid / 0.85) * 0.3) # add some power currently used from grid
            
            # Slow down if almost empty
            if battery_soc < 30:
                max_discharge_power_1040 = max_discharge_power_1040 / 2
            elif battery_soc < 20:
                max_discharge_power_1040 = max_discharge_power_1040 / 4                
            elif battery_soc < 10:
                max_discharge_power_1040 = max_discharge_power_1040 / 6                                
                
            new_discharge_power = min(new_discharge_power, max_discharge_power_1040) # limit discharging power
            new_battery_power = new_discharge_power


    if grid_power < 0:  # If power is feed to grid --> Try to CHARGE the battery more  
        if battery_soc < battery_soc_max_1044:  # If battery not full
            new_charge_power = battery_power # reuse any existing charge power 
            new_charge_power = min(new_charge_power, 0) # avoid positive values that would discharge the battery 
            new_charge_power = new_charge_power + ((grid_power / 0.85) * 0.3) # add some power currently feed to grid
            new_charge_power = max(new_charge_power, max_charge_power_1038) # Do not exceed max charge power
            new_battery_power = new_charge_power


    # Write result via modbus to Kostal Inverter
    log.info(new_battery_power)
    write_kostal(value=new_battery_power)


def write_kostal(value):

    client = ModbusTcpClient(host="192.168.178.59", port=1502)
    client.connect()

    # 1034: {"description": "Battery charge power (DC) setpoint, absolute", "unit": "W", "format": "Float", "access": "RW"},

    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder.add_32bit_float(value)
    payload = builder.build()

    response = client.write_registers(address=1034,
                                        values=payload,
                                        slave=71,
                                        skip_encode=True)

    client.close()

    return None