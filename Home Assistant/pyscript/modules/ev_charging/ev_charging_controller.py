from influxdb import DataFrameClient #v1 https://github.com/influxdata/influxdb-python
import pandas as pd
import time

def ev_charging_controller(pyscript_app_config):

    ##############################
    # Hole Inputs
    ##############################

    # Hole gewünschten Ziel SOC des E-Autos
    # In Prozent von 0 bis 100
    # Dieser Action Value kann vom User oder von Automatisierung gesetzt worden sein
    ev_soc_soll = get_ev_soc_soll(pyscript_app_config)

    
    # Hole aktuellen SOC vom E-Auto (ZOE)
    # In Prozent von 0 bis 100
    try:
        ev_soc_ist = int(sensor.zoe_batteriestand)
    except:
        log.warning("Kein aktueller Batteriestand des Elektroautos gefunden")
        ev_soc_ist = 999

        # Versuch den Sensor wiederherzustellen
        script.zoe_reload_integration()
        time.sleep(10) # Sleep for 3 seconds



    # Hole maximalwert des SOC vom E-Auto
    # In Prozent von 0 bis 100
    try:
        ev_soc_max = 85 #TODO per Sensor
    except:
        ev_soc_max = 85


    # Hole die aktuelle Leistung des Netzanschlusses
    # In Watt. 
    # Positive und negative Werte sind möglich
    try:
        grid_power_watt = int(sensor.scb_grid_power)
    except:
        log.warning("Keine aktuelle Netzleistung gefunden")
        grid_power_watt = 0


    # Hole den aktuellen SOC des Heimspeichers
    # In Prozent von 0 bis 100
    try:
        battery_soc_ist = int(sensor.scb_battery_soc)
    except:
        log.warning("Kein aktueller Batteriestand des Heimspeichers gefunden")
        battery_soc_ist = 0


    # Hole den maximal erlaubten SOC des Heimspeichers
    # In Prozent von 0 bis 100
    try:
        battery_soc_max = 95 #TODO per Sensor
    except:
        battery_soc_max = 95       


    # Hole bisherigen Lademodus
    # Optionen:
    # 0 --> Zuletzt keine Beladung
    # 1 --> Zuletzt Beladung aus Netz (wenn nötig) und PV (wenn vorhanden)
    # 2 --> Zuletzt nur Beladung mit PV Überschuss
    try:
        lademodus = pyscript.ev_charging_controller_lademodus
    except:
        log.warning("Kein aktueller Lademodus gefunden")
        lademodus = 0

    # Hole die Speicherkapazität des Autos
    try:
        ev_capacity_kwh = 50 #TODO per Sensor
    except:
        ev_capacity_kwh = 50



    ############################
    # Berechne Outputs
    ############################

    # Grundsätzlich soll nicht geladen werden
    ladeleistung_soll_kw = 0

    # Laden, wenn das Auto weniger geladen ist als gewünscht
    # Dabei soll die Beladung möglichst 1 Stunde lang erfolgen
    if ev_soc_ist < ev_soc_soll:

        # Wieviele kW müssen 1 Stunde geladen werden um Zielladung zu erreichen?
        # Ladeleistung aus Energiedifferenz ermitteln
        ev_energy_ist = ev_capacity_kwh * ev_soc_ist
        ev_energy_soll = ev_capacity_kwh * ev_soc_soll
        ladeleistung_soll_kw = ev_energy_soll - ev_energy_ist

        # Minimale Leistung sicherstellen
        if ladeleistung_soll_kw < 1.4:
            ladeleistung_soll_kw = 1.4

        # Maximale Leistung begrenzen
        if ladeleistung_soll_kw > 22:
            ladeleistung_soll_kw = 23

        # Notiere Lademodus
        lademodus = 1




    # PV-Überschuss laden
    if ev_soc_ist < ev_soc_max:

        # Wenn Lademodus 1 bereits eine Leistung vorgibt, diese beibehalten
        if lademodus != 1:
            
            # Erst Überschuss für Heimspeicher nutzen, statt fürs Auto
            if battery_soc_ist >= battery_soc_max:

                # Ermitteln wieviel ins Netz eingespeist wird
                # Bei Netzeinspeisung ist grid_power negativ
                # Um den Wert nutzen zu können drehen wir in um  
                if grid_power_watt < 0:
                    einspeisung_netz_watt = grid_power_watt * -1
                else:
                    einspeisung_netz_watt = 0        

                # Wenn initial genug PV Überschuss besteht oder wenn bereits Überschuss geladen wird
                if einspeisung_netz_watt >= 2000 or lademodus == 2:

                    # Umrechnen in Kilowatt
                    ladeleistung_soll_kw = einspeisung_netz_watt / 1000

                    # Maximale Leistung begrenzen
                    if ladeleistung_soll_kw > 22:
                        ladeleistung_soll_kw = 23

                    # Notiere Lademodus
                    lademodus = 2




    # Wir haben bis hier hin die gewünschte Ladeleistung in KW bestimmt
    # Die Wallbox wird jedoch mittels Setzen von Ampere und Phase gesteuert
    if ladeleistung_soll_kw >= 1.4:
        # Laden wenn die minimale Ladeleistung der Wallbox erreicht wird
        phase_soll, ampere_soll = kw_to_phase_ampere(kw=ladeleistung_soll_kw)
        state_soll = "2: On"

    # Beladung beenden
    else:
        phase_soll = "1: 1-Phasig"
        ampere_soll = 6
        state_soll = "1: Off"
        lademodus = 0                



    ##################################
    # Setze Outputs (Controll Wallbox)
    ###################################

    # Sende Werte an Wallbox
    script.goe_set_ampere(ampere=ampere_soll)
    script.goe_set_phase(phase=phase_soll)    
    script.goe_set_state(state=state_soll)

    # Sende Werte an Pyscript Variablen
    pyscript.ev_charging_controller_lademodus = lademodus



def get_ev_soc_soll(pyscript_app_config):

    # Wenn auch die vom User gesetzten Werte berücksichtigt werden sollen,
    # reicht es nicht nur den Sensor auszulesen. 
    # Die User gesetzen Werte sind in der InfluxDB

    # Ansonsten würde dieser Teil reichen
    # try:
    #     ev_soc_soll = int(sensor.ev_charging_action_target_soc)
    # except:
    #     ev_soc_soll = 0    

    try:
        # pyscript_app_config kommt von der pyscript.app_config
        host = pyscript_app_config.get("host")
        port = pyscript_app_config.get("port")
        username = pyscript_app_config.get("username")
        password = pyscript_app_config.get("password")
        database = pyscript_app_config.get("database")

        # InfluxDB Connection
        client = DataFrameClient(host,port,username,password,database)

        # Get Zielwert
        query_string = '''
        SELECT "value"
        FROM "home_assistant"."autogen"."%"
        WHERE "entity_id" = 'ev_charging_action_target_soc'
        '''

        response = task.executor(client.query, query_string)
        client.close()

        # Prepare Data
        data_df = response['%'].copy()
        data_df.index = data_df.index.tz_convert('Europe/Berlin')
        data_df.reset_index(inplace=True)

        # Get most recent value
        current_time = pd.Timestamp.now(tz='Europe/Berlin')
        data_df = data_df.query('index <= "%s"' % current_time).copy()
        last_value_setted = data_df.iloc[-1].value

        ev_soc_soll = last_value_setted
    

    # Bei Fehler nehmen wir an, dass nicht geladen werden soll
    except:
        log.error('exception when processing parameters: ' + str(locals()))
        ev_soc_soll = 0

    return ev_soc_soll




# Auf Basis der Leistung die Phase und Ampere für die Wallbox bestimmen
def kw_to_phase_ampere(kw):

    # Mappings
    one_phase_mapping = {
        6: 1.4,
        7: 1.6,
        8: 1.8,
        9: 2.1,
        10: 2.3,
        11: 2.5,
        12: 2.8,
        13: 3.0,
        14: 3.2,
        15: 3.5,
        16: 3.7,
        17: 3.9,
        18: 4.1,
        19: 4.4,
        20: 4.6,
        21: 4.8,
        22: 5.1,
        23: 5.3,
        24: 5.5,
        25: 5.8,
        26: 6.0,
        27: 6.2,
        28: 6.4,
        29: 6.7,
        30: 6.9,
        31: 7.1,
        32: 7.4
    }

    three_phase_mapping = {
        7: 4.8,
        8: 5.5,
        9: 6.2,
        10: 6.9,
        11: 7.6,
        12: 8.3,
        13: 9.0,
        14: 9.7,
        15: 10.4,
        16: 11.0,
        17: 11.7,
        18: 12.4,
        19: 13.1,
        20: 13.8,
        21: 14.5,
        22: 15.2,
        23: 15.9,
        24: 16.6,
        25: 17.3,
        26: 17.9,
        27: 18.6,
        28: 19.3,
        29: 20.0,
        30: 20.7,
        31: 21.4,
        32: 22.1
    }

    # Kleine Leistungen sind 1 Phasig zu laden.
    if kw <= 7.4:
        mapping = one_phase_mapping
        phase = "1: 1-Phasig"

    else:
        mapping = three_phase_mapping
        phase = "2: 3-Phasig"

        
    # Finden Sie den passenden Ampere-Wert.
    chosen_ampere = None
    
    # Finde den nächstkleineren kW Wert
    for ampere, max_kw in reversed(sorted(mapping.items())):
        
        if kw >= max_kw:
            chosen_ampere = ampere
            break


    return phase, chosen_ampere    




