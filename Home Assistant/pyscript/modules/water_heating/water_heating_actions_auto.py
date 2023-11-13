from datetime import datetime
import time

def water_heating_actions_auto():

    # get current datetime
    dt = datetime.now()
    # get day of week as an integer, Monday is 0
    weekday = dt.weekday()

    # Temperatur in Abhängigkeit vom Strompreis steuern
    # Wie günstig oder teuer ist der Strom aktuell?
    # Von 0 (günstigste Stunde) bis 23 (teuerste Stunde)
    try:
        epex_rank = int(sensor.epex_spot_de_lu_rank)
    except:
        log.warning("EPEX Daten fehlen")  
        # Wenn Sensor nicht verfügbar, dann nehmen wir Worst Case an
        epex_rank = 999
        
        # Versuch den Sensor wiederherzustellen
        script.epex_reload_integration()    
        time.sleep(10) # Sleep for 3 seconds    

    # Temperatur in Abhängigkeit vom Strompreis steuern
    if epex_rank == 0:
        # In der günstigsten Stunde die Temperatur halten
        ziel_temp_wasser = 48

    if epex_rank == 1:
        # In der zweit-günstigsten Stunde die Temperatur extra erhöhen
        # Die günstigste Stunde wird schon für die Raumheizung genutzt
        ziel_temp_wasser = 55

        if weekday == 5:
            # Einmal die Woche Legionellen abkochen
            ziel_temp_wasser = 60

    if epex_rank >= 2 and epex_rank <= 11:
        # In den günstigsten Stunde die Temperatur halten
        ziel_temp_wasser = 48

    if epex_rank >= 12:
        # In den teuersten Stunden die Temperatur aufs Minimum setzen
        ziel_temp_wasser = 30
        
    # Ergebnis runden
    ziel_temp_wasser = round(ziel_temp_wasser, 1)


    # Ergebnis im Sensor sichern
    sensor.isg_warmwasser_zieltemperatur = ziel_temp_wasser
    sensor.isg_warmwasser_zieltemperatur.unit_of_measurement = "°C"
    sensor.isg_warmwasser_zieltemperatur.friendly_name = "ISG Warmwasser Zieltemperatur"
    sensor.isg_warmwasser_zieltemperatur.herkunft = "custom_components.pyscript.apps.water_heating_actions_auto"
    sensor.isg_warmwasser_zieltemperatur.epex_rank = epex_rank
