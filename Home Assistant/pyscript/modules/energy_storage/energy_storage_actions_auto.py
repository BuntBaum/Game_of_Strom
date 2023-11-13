import datetime
import pandas as pd
import time

# Legt fest wieviel Energie mindestens im Heimspeicher sein soll (SOC MIN)
# Nutzt die aktuellen Strompreise
# Ermittelt die Preis-Minima und den Durchschnittspreis
# Grundsätzlich den Speicher freigeben     
# Wenn lokales Minima erreicht wird, dann Speicher laden
# Anschließend Energie halten
# Erst in nächster überdurchschnittlich teuren Phase wieder freigeben


def energy_storage_actions_auto():

    # Zum Aufbau des Preis-Dataframe
    start_times = []
    prices = []

    
    # Test und Reload des Sensors
    try:
        _ =  float(sensor.epex_spot_de_lu_price.price_ct_per_kwh)
    except:
        log.warning("EPEX Daten fehlen")       
        # Versuch den Sensor wiederherzustellen
        script.epex_reload_integration()     
        time.sleep(10) # Sleep for 3 seconds  


    # Die aktuellen Preise auslesen und als Dataframe speichern. Umfasst auch vorherigen und nächsten Tag
    for price in sensor.epex_spot_de_lu_price.data:        
        start_times.append(price['start_time'])
        prices.append(price['price_ct_per_kwh'])                

    df = pd.DataFrame({
        'Timestamp': start_times,
        'Price': prices
    })


    # Den Zeitstempel in Berliner Zeit als Index nutzen
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    df.index = df.index.tz_convert('Europe/Berlin')      

    # Das heutige Datum im gleichen Format wie den Zeitindex erhalten
    today = pd.Timestamp.now(tz='Europe/Berlin').strftime('%Y-%m-%d')

    # Wir brauchen nur die heutigen Preise
    df_today = df.loc[today].copy()

    # Lokale Minima ermitteln
    # über mehrere Tage
    shifted_series_1 = df['Price'].shift(1)
    shifted_series_2 = df['Price'].shift(-1)
    condition1 = df['Price'].lt(shifted_series_1)
    condition2 = df['Price'].lt(shifted_series_2)
    local_minima = condition1 & condition2


    # Überdurchschnittliche heutige Preise ermitteln
    average_price = df_today['Price'].mean()
    above_average = df['Price'].gt(average_price)



    # Wie wieviele lokale Minima sind heute günstiger als der Durchschnittspreis?
    local_minima.name = "local_min"
    above_average.name = "above_avg"
    df_test = pd.concat([local_minima, above_average], axis=1)
    df_test = df_test.loc[today]
    df_test = df_test.query("local_min == True and above_avg == False")
    anzahl_minima = len(df_test)

    # Wenn es heute nur ein günstiges Minima gibt, dann dieses voll ausnutzen
    # Ansonsten reicht der halbe Speicher (und lässt Platz für PV-Überschuss)
    if anzahl_minima == 1:
        soc_minima = 95
    else:
        soc_minima = 55

    df_today['SOC_MIN'] = None

    normal_soc = 5


    # Grundsätzlich den Speicher freigeben     
    # Wenn lokales Minima erreicht wird, dann Speicher laden
    # Anschließend Energie halten
    # Erst in nächster teuren Phase wieder freigeben
    current_soc = normal_soc
    for idx, row in df_today.iterrows():
        
        if local_minima[idx]:
            current_soc = soc_minima

        if above_average[idx]:
            current_soc = normal_soc

        df_today.loc[idx, 'SOC_MIN'] = current_soc    
        

    # Den SOC_MIN für die aktuelle Stunde aus dem DataFrame abrufen
    current_time = pd.Timestamp.now(tz='Europe/Berlin')
    df_today.reset_index(inplace=True)  
    df_today = df_today.query('Timestamp <= "%s"' % current_time).copy()    
    current_soc_min = df_today.iloc[-1].SOC_MIN




    # Ergebnis im Sensor speichern
    sensor.kostal_battery_soc_min_action = current_soc_min
    sensor.kostal_battery_soc_min_action.unit_of_measurement = "%"
    sensor.kostal_battery_soc_min_action.friendly_name = "Kostal Battery Min Soc Action"
    sensor.kostal_battery_soc_min_action.herkunft = "custom_components.pyscript.apps.kostal_battery_control"




