from influxdb import DataFrameClient #v1 https://github.com/influxdata/influxdb-python
import pandas as pd


def water_heating_controller(pyscript_app_config):

    # InfluxDB Connection
    client = DataFrameClient(host=get_config(pyscript_app_config, 'host'),
                                port=get_config(pyscript_app_config, 'port'),
                                username=get_config(pyscript_app_config, 'username'),
                                password=get_config(pyscript_app_config, 'password'),
                                database=get_config(pyscript_app_config, 'database'))

    # Get Zieltemperaturen
    query_string = '''
    SELECT "value"
    FROM "home_assistant"."autogen"."°C"
    WHERE "entity_id" = 'isg_warmwasser_zieltemperatur'
    '''
    
    # Query InfluxDB
    try:
        log.debug(client)    
        response = task.executor(client.query, query_string)
    except:
        log.error('exception when processing parameters: ' + str(locals()))
        raise
    client.close()

    # Prepare Data
    data_df = response['°C'].copy()
    data_df.index = data_df.index.tz_convert('Europe/Berlin')
    data_df.reset_index(inplace=True)

    # Get most recent target temperature
    current_time = pd.Timestamp.now(tz='Europe/Berlin')
    data_df = data_df.query('index <= "%s"' % current_time).copy()
    last_value_setted = data_df.iloc[-1].value
    
    # Write value to Stiebel
    script.isg_set_komfort_temperatur_warmwasser(komforttemperatur_warmwasser=last_value_setted)




# Get configuration from Pyscript
def get_config(pyscript_app_config, name):
    
    value = pyscript_app_config.get(name)
    # value = pyscript.app_config.get(name)
    if value is None:
        log.error('"' + name + '" is required parameter but not defined in Pyscript configuration for application')
    return value