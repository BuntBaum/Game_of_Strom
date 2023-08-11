from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder



@time_trigger("period(0:00, 1 sec)") # This will trigger every 1 second
def kostal_battery_control():
    log.info("Hallo Battery Control")

    # The following sensores are made available via Kostal Integration (via REST-API)
    # https://www.home-assistant.io/integrations/kostal_plenticore/    
    home_power_from_grid = int(sensor.scb_home_power_from_grid) 
    grid_power = int(sensor.scb_grid_power)
    battery_power = int(sensor.scb_battery_power)
    battery_soc = int(sensor.scb_battery_soc)
    battery_soc_min = int(number.scb_battery_min_soc)

    # These could be made available via Kostal Modbus or just set here
    max_discharge_power_1040 = 2750
    max_charge_power_1038 = -2750
    battery_soc_max_1044 = 95

    log.info("home_power_from_grid: " + str(home_power_from_grid))
    log.info("grid_power: " + str(grid_power))
    log.info("battery_power: " + str(battery_power))
    log.info("battery_soc: " + str(battery_soc))
    log.info("battery_soc_min: " + str(battery_soc_min))
    log.info("max_discharge_power_1040: " + str(max_discharge_power_1040))
    log.info("max_charge_power_1038: " + str(max_charge_power_1038))
    log.info("battery_soc_max_1044: " + str(battery_soc_max_1044))


    # Reuse existing power value
    # Battery will discharge if this value is > 0 and charge if it is < 0
    new_battery_power = battery_power 

    if battery_soc < battery_soc_min: # If Battery should be charged --> CHARGE battery more
        log.info("CHARGE battery more")
        new_battery_power = max_charge_power_1038


    if home_power_from_grid > 0: # If Power is taken from the grid for home consumption --> Try to DISCHARGE the battery more
        log.info("Trying to DISCHARGE the battery more")
        
        if battery_soc > battery_soc_min: # If Battery not empty
            log.info("Battery not empty")                        
            
            # As the power currently used from grid for home is positive, this will increase the battery power
            # if battery power is positive, battery will be discharged
            new_battery_power = new_battery_power + home_power_from_grid 
            
            # Slow down if SOC is close to min SOC
            soc_distance = battery_soc - battery_soc_min
            if soc_distance < 5:
                log.info("SOC is close to min SOC")
                new_battery_power = new_battery_power / 2

            # Slow down if almost empty
            if battery_soc < 30:
                log.info("battery_soc < 30")
                max_discharge_power_1040 = max_discharge_power_1040 / 2
            elif battery_soc < 20:
                log.info("battery_soc < 20")
                max_discharge_power_1040 = max_discharge_power_1040 / 4                
            elif battery_soc < 10:
                log.info("battery_soc < 10")
                max_discharge_power_1040 = max_discharge_power_1040 / 6                                
                
            # make sure to limit discharging power
            new_battery_power = min(new_battery_power, max_discharge_power_1040) 


    if grid_power < 0:  # If power is feed to grid --> Try to CHARGE the battery more
        log.info("trying to CHARGE the battery more")  
        
        if battery_soc < battery_soc_max_1044:  # If battery not full
            log.info("battery not full")            

            # as the power currently feed to grid is a negative value, this will decrease the battery power
            # if battery power is negative, battery will be charged
            new_battery_power = new_battery_power + grid_power 

            # make sure to limit charging power
            new_battery_power = max(new_battery_power, max_charge_power_1038)



    # Write result via modbus to Kostal Inverter
    log.info("new_battery_power: " + str(new_battery_power))
    write_kostal(value=new_battery_power)


def write_kostal(value):

    client = ModbusTcpClient(host="192.168.178.59", port=1502)
    client.connect()

    # Address 1034
    # Battery charge power (DC) setpoint, absolute
    # unit: "W"
    # format: "Float"
    # access: "ReadWrite"
    modbus_adress = 1034

    # Make sure to have selected the correct Big Endian Settings in Kostel Inverter
    builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
    builder.add_32bit_float(value)
    payload = builder.build()

    response = client.write_registers(  address=modbus_adress,
                                        values=payload,
                                        slave=71,
                                        skip_encode=True)

    client.close()
