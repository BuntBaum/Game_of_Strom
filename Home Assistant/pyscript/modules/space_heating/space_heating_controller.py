from influxdb import DataFrameClient #v1 https://github.com/influxdata/influxdb-python
import pandas as pd

def space_heating_controller(pyscript_app_config):

    # InfluxDB Connection
    client = DataFrameClient(host=get_config(pyscript_app_config,'host'),
                                port=get_config(pyscript_app_config, 'port'),
                                username=get_config(pyscript_app_config, 'username'),
                                password=get_config(pyscript_app_config, 'password'),
                                database=get_config(pyscript_app_config, 'database'))   

    # Get Zieltemperaturen
    query_string = '''
    SELECT "value"
    FROM "home_assistant"."autogen"."°C"
    WHERE "entity_id" = 'isg_heizkreis_zieltemperatur'
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
    if last_value_setted > 70:
        # Es geht nur bis 70 Grad
        last_value_setted = 70

    if last_value_setted >= 20:
        script.isg_set_festwert_temperatur(festwert_temperatur=last_value_setted)
    elif last_value_setted < 20:
        # Der minimale Wert is 20, also Festwertbetrieb ausstellen.
        # Dann übernimmt wieder Programmbetrieb der WP
        script.isg_set_festwertbetrieb_ausstellen(aus_wert="AUS")


# Get configuration from Pyscript
def get_config(pyscript_app_config, name):
    value = pyscript_app_config.get(name)
    if value is None:
        log.error('"' + name + '" is required parameter but not defined in Pyscript configuration for application')
    return value



# Steuert die Ventile der Heizkörper
# In den Schlafzimmern wird Nachts runtergedreht
def space_heating_hkr_controller():

    # Um die aktuelle Uhrzeit zu ermitteln
    now = pd.Timestamp.now(tz='Europe/Berlin')

    # Tagsüber alle Heizkörper maximal aufdrehen
    if now.hour >= 7 and now.hour < 21:
        log.info("Alle HKR aufdrehen")
        hkr_temperature = 30
        script.hkr_set_temperature(temperature=hkr_temperature)

    # Nachts die Heizkörper in den Schlafzimmern dimmen wegen Geräuschen
    else:
        log.info("HKR in den Schlafzimmern dimmen")
        hkr_temperature = 18
        climate.set_temperature(temperature=hkr_temperature, entity_id="climate.hkr_og_schlafzi")
        climate.set_temperature(temperature=hkr_temperature, entity_id="climate.hkr_og_ole")    