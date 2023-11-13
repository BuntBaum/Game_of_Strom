import time

def ev_charging_actions_auto():

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

    
    # Wie teuer ist der Strom aus dem Netz in Cent? (Börsen-Netto-Preis)
    try:
        price_ct_per_kwh =  float(sensor.epex_spot_de_lu_price.price_ct_per_kwh)
    except:
        log.warning("EPEX Daten fehlen")  
        # Wenn Sensor nicht verfügbar, dann nehmen wir Worst Case an
        price_ct_per_kwh = 999
        
        # Versuch den Sensor wiederherzustellen
        script.epex_reload_integration()    
        time.sleep(10) # Sleep for 3 seconds


    # Zur günstigsten Stunde des Tages, bei höheren Preisen
    if epex_rank == 0 and price_ct_per_kwh > 3:
        ev_charging_action_target_soc = 50

    # Zur günstigsten Stunde des Tages, bei geringen Preisen
    elif epex_rank == 0 and price_ct_per_kwh <= 3:
        ev_charging_action_target_soc = 80
    
    # In den 4 günstigsten Stunden
    elif epex_rank <= 3:
        ev_charging_action_target_soc = 30

    # In den 6 günstigsten Stunden
    elif epex_rank <= 5:
        ev_charging_action_target_soc = 20

    # In den 11 günstigsten Stunden
    elif epex_rank <= 10:
        ev_charging_action_target_soc = 10

    # Basisbeladung sicherstellen
    else:
        ev_charging_action_target_soc = 5



    # Als Action wird der benötigte State of Charge (SOC) für das Elektroauto gesetzt
    # Ergebnis im Sensor speichern
    sensor.ev_charging_action_target_soc = ev_charging_action_target_soc
    sensor.ev_charging_action_target_soc.unit_of_measurement = "%"
    sensor.ev_charging_action_target_soc.friendly_name = "EV Charging Action Target SOC"
    sensor.ev_charging_action_target_soc.herkunft = "Pyscript ev_charging_actions_auto"
    sensor.ev_charging_action_target_soc.epex_rank = epex_rank
    sensor.ev_charging_action_target_soc.price_ct_per_kwh = price_ct_per_kwh
