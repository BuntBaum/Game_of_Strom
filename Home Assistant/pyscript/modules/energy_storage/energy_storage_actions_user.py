from influxdb import InfluxDBClient #v1 https://github.com/influxdata/influxdb-python
import requests
import pandas as pd
import json



def energy_storage_actions_user(pyscript_app_config):

    
    # Get Annotations from Grafana via API
    api_token_viewer = get_config(pyscript_app_config, 'viewer_token')
    headers = {'Authorization': 'Bearer ' + api_token_viewer}
    url = 'http://a0d7b954-grafana:3000/api/annotations'
    response = task.executor(requests.get, url, headers=headers)

    # Prepare Annotations
    annotations = response.json()
    annotations_df = pd.DataFrame(annotations)
    annotations_df = annotations_df[['dashboardId', 'panelId', 'id', 'time', 'timeEnd', 'text', 'tags']].copy() #Only relevant columns

    # Unix-Timestamp to Datetime
    annotations_df['time'] = pd.to_datetime(annotations_df['time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Berlin')
    annotations_df['timeEnd'] = pd.to_datetime(annotations_df['timeEnd'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Europe/Berlin')
    
    # Only Process future annotations
    current_time = pd.Timestamp.now(tz='Europe/Berlin')
    annotations_df = annotations_df.query('time > "%s"' % current_time).copy() # Only future annotations

    # Only use Annotations for Warmwater and Battery-MinSOC
    kostal_set_socmin = annotations_df.query('dashboardId == 4 and panelId == 2').copy() # action panel battery


    # Verarbeite Annotation
    entity_id = "kostal_battery_soc_min_action"
    measurement = "%"
    tags = {
            "state_class_str": "measurement",
            "entity_id": entity_id,
            "friendly_name": "Kostal Battery Min Soc Action",
            "source": "energy_storage_actions_user"
            }  
    datapoint_list = []

    for annotation in kostal_set_socmin.itertuples():
        
        if annotation.text == "delete":
            delete_in_influxdb(pyscript_app_config, annotation, entity_id, measurement)

        else:
            datapoint = {"measurement": measurement,
                        "time": annotation.time,
                        "fields": {
                            "value": float(annotation.text)
                            }
                        }
            datapoint_list.append(datapoint)        

        # delete annotation after processing
        _ = delete_annotation(pyscript_app_config, annotation.id)


    # Write Annotation Value
    _ = write_to_influxdb(pyscript_app_config, datapoint_list, tags)

















def delete_annotation(pyscript_app_config, annotation_id):
    # delete annotation
    url = f'http://a0d7b954-grafana:3000/api/annotations/{annotation_id}'
    api_token_writer = get_config(pyscript_app_config, 'writer_token')
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token_writer}",
    }
    response = task.executor(requests.delete, url, headers=headers)
#

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

def delete_in_influxdb(pyscript_app_config, annotation, entity_id, measurement):

    # Delete values in InfluxDB
    start = annotation.time
    start = start.tz_convert('UTC')
    start = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
    stop = annotation.timeEnd
    stop = stop.tz_convert('UTC')
    stop = stop.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    query = '''
            DELETE FROM "{}" 
            WHERE "entity_id" = '{}'
            AND time >= '{}'
            AND time <= '{}'
            '''.format(measurement, entity_id ,start, stop)


    # Call InfluxDB to execute query
    client = InfluxDBClient(host=get_config(pyscript_app_config, 'host'),
                                port=get_config(pyscript_app_config, 'port'),
                                username=get_config(pyscript_app_config, 'username'),
                                password=get_config(pyscript_app_config, 'password'),
                                database=get_config(pyscript_app_config, 'database'))
    try:
        log.debug(client)    
        response = task.executor(client.query, query)
    except:
        log.error('exception when processing parameters: ' + str(locals()))
        raise

    client.close()    




# Get configuration from Pyscript
def get_config(pyscript_app_config, name):
    value = pyscript_app_config.get(name)
    if value is None:
        log.error('"' + name + '" is required parameter but not defined in Pyscript configuration for application')
    return value