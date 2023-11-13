



def space_heating_actions_auto():


    # Konstanten setzen
    ziel_temp_innen = 21 # Welche Innentemperatur wird im Haus gewünscht?
    steigung_innen = 3.0 # Wie sehr soll eine Abweichungen von der gewünschten Innentemp korrigiert werden?
    steigung_aussen = 1.0 # Steigung der Heizkurve für Abweichung der Außentemperatur von Referenz-Außentemp


    # Innentemperatur berechnen
    ist_temp_innen_1 = float(sensor.innentemperatur_erdgeschoss)
    ist_temp_innen_2 = float(sensor.innentemperatur_obergeschoss)
    ist_temp_innen = (ist_temp_innen_1 + ist_temp_innen_2) / 2 # Mittelwert der beiden Sensoren
    ist_temp_innen = round(ist_temp_innen, 1)



    # Außentemperatur berechnen
    ist_temp_aussen_1 = float(sensor.hohenholte_temperatur)
    ist_temp_aussen_2 = float(sensor.isg_aussentemperatur)
    ist_temp_aussen = (ist_temp_aussen_1 + ist_temp_aussen_2) / 2 # MW der beiden Sensoren
    ist_temp_aussen = round(ist_temp_aussen, 1)


    # Korrekturwert für Abweichungen der Innentemperatur von Ziel-Temperatur
    delta_innen = ziel_temp_innen - ist_temp_innen
    korrektur_temp_innen = steigung_innen * delta_innen


    # Korrekturwert für Abweichungen der Außentemperatur von Ziel-Temperatur
    delta_aussen = ziel_temp_innen - ist_temp_aussen # innen-zieltemp wird hier auch als Referenz genutzt
    korrektur_temp_aussen = steigung_aussen * delta_aussen


    # Ergebnis: benötigte Soll-Vorlauftemperatur
    vorlauf_temp_hk = ziel_temp_innen + korrektur_temp_innen + korrektur_temp_aussen

    # Als Info tracken
    vorlauf_temp_hk_raw = vorlauf_temp_hk

    # Berücksichtigung der minimal möglichen Temperatur
    if vorlauf_temp_hk < 20:
        # Festwert-Temperatur muss mindestens 20 Grad sein
        vorlauf_temp_hk = 20

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



    if epex_rank >= 12:
        # In den teuersten 12 Stunden die Temperatur aufs Minimum setzen
        vorlauf_temp_hk = 20

    if epex_rank == 0:
        # In der günstigsten Stunde die Temperatur extra erhöhen
        vorlauf_temp_hk = vorlauf_temp_hk * 1.20
        
    # Ergebnis runden
    vorlauf_temp_hk = round(vorlauf_temp_hk, 1)


    sensor.isg_heizkreis_zieltemperatur = vorlauf_temp_hk
    sensor.isg_heizkreis_zieltemperatur.vorlauf_temp_hk_raw = vorlauf_temp_hk_raw
    sensor.isg_heizkreis_zieltemperatur.unit_of_measurement = "°C"
    sensor.isg_heizkreis_zieltemperatur.friendly_name = "ISG Heizkreis Zieltemperatur"
    sensor.isg_heizkreis_zieltemperatur.herkunft = "custom_components.pyscript.apps.space_heating_actions_auto"
    sensor.isg_heizkreis_zieltemperatur.ziel_temp_innen = ziel_temp_innen
    sensor.isg_heizkreis_zieltemperatur.ist_temp_innen = ist_temp_innen
    sensor.isg_heizkreis_zieltemperatur.korrektur_temp_innen = korrektur_temp_innen
    sensor.isg_heizkreis_zieltemperatur.ist_temp_aussen = ist_temp_aussen
    sensor.isg_heizkreis_zieltemperatur.korrektur_temp_aussen = korrektur_temp_aussen
    sensor.isg_heizkreis_zieltemperatur.epex_rank = epex_rank


