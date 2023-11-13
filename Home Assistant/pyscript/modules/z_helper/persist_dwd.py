from influxdb import InfluxDBClient #v1 https://github.com/influxdata/influxdb-python


def persist_dwd(pyscript_app_config):


    datapoint_list = create_datapoints(sensor=sensor.hohenholte_sonnenscheindauer.data, measurement="s")

    tags = {
        "state_class_str": "measurement",
        "entity_id": "sun_duration_hohenholte",
        "friendly_name": "Sun Duration hohenholte",
        "domain": "sensor",
        "source": "pyscript.dwd_to_influxdb"
        }

    write_to_influxdb(pyscript_app_config, datapoint_list, tags)




    datapoint_list = create_datapoints(sensor=sensor.hohenholte_sonneneinstrahlung.data, measurement="W/m^2")

    tags = {
        "state_class_str": "measurement",
        "entity_id": "sun_irradiance_hohenholte",
        "friendly_name": "Sun Irradiance hohenholte",
        "domain": "sensor",
        "source": "pyscript.dwd_to_influxdb"
        }

    write_to_influxdb(pyscript_app_config, datapoint_list, tags)




    datapoint_list = create_datapoints(sensor=sensor.hohenholte_temperatur.data, measurement="°C")

    tags = {
        "state_class_str": "measurement",
        "entity_id": "temperature_hohenholte",
        "friendly_name": "Temperature hohenholte",
        "domain": "sensor",
        "source": "pyscript.dwd_to_influxdb"
        }

    write_to_influxdb(pyscript_app_config, datapoint_list, tags)


    return None


# Get configuration from Pyscript
def get_config(pyscript_app_config, name):
    value = pyscript_app_config.get(name)
    if value is None:
        log.error('"' + name + '" is required parameter but not defined in Pyscript configuration for application')
    return value





def create_datapoints(sensor, measurement):

    datapoint_list = []
    for data in sensor:
        log.debug(data)

        datapoint = {
                    "measurement": measurement,
                    "time": data['datetime'],
                    "fields": {
                                "value": data['value']
                                }
                    }
        datapoint_list.append(datapoint)

    return datapoint_list


def write_to_influxdb(pyscript_app_config, datapoint_list, tags):

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