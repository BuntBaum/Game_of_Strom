from influxdb import InfluxDBClient #v1 https://github.com/influxdata/influxdb-python
import pandas as pd



def persist_epex(pyscript_app_config):
    
    datapoint_list = []
    for price in sensor.epex_spot_de_lu_price.data:
        log.debug(price)

        datapoint = {
                    "measurement": "EUR/MWh",        
                    "time": price['start_time'],
                    "fields": {
                                "value": price['price_eur_per_mwh'],
                                "price_ct_per_kwh": price['price_ct_per_kwh']
                                }
                    }
        datapoint_list.append(datapoint)

    tags = {
            "state_class_str": "measurement",
            "entity_id": "epex_spot_de_lu_price",
            "friendly_name": "EPEX Spot DE-LU Price",
            "domain": "sensor",
            "source": "pyscript.epex_price_to_influxdb"
            }        

    # Call InfluxDB to execute query
    client = InfluxDBClient(host=get_config(pyscript_app_config, 'host'),
                            port=get_config(pyscript_app_config, 'port'),
                            username=get_config(pyscript_app_config, 'username'),
                            password=get_config(pyscript_app_config, 'password'),
                            database=get_config(pyscript_app_config, 'database'))
    try:
        log.debug(client)    
        response = task.executor(client.write_points, points=datapoint_list, tags=tags)
    except:
        log.error('exception when processing parameters: ' + str(locals()))
        raise
    client.close()

    return None


# Get configuration from Pyscript
def get_config(pyscript_app_config, name):
    value = pyscript_app_config.get(name)
    if value is None:
        log.error('"' + name + '" is required parameter but not defined in Pyscript configuration for application')
    return value

