# @service
# @time_trigger('cron(58 * * * *)')  # 2 Minuten vor jeder vollen Stunde
def water_heating_reward():
    
    # Nach HA Neustart ist Sensor nicht mehr da
    # returns all HASS state variable (entity) names
    entities = state.names(domain=None)    
    if "sensor.isg_warmwasser_reward" not in entities:
        # Sensor initialisieren
        sensor.isg_warmwasser_reward = 0

    # Werte auslesen
    ist_temperatur = float(sensor.isg_isttemperatur_ww)
    kosten = float(sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich)
    soll_temperatur = 48
    normalisierungsfaktor = 4

    # Reward Warmwasser
    reward = reward_function(soll_temperatur, ist_temperatur, kosten, normalisierungsfaktor)

    # Ergebnis im Sensor speichern
    sensor.isg_warmwasser_reward = reward
    sensor.isg_warmwasser_reward.friendly_name = "ISG Warmwater Reward"
    sensor.isg_warmwasser_reward.herkunft = "custom_components.pyscript.apps.water_heating_reward"
    sensor.isg_warmwasser_reward.unit_of_measurement = "state"


def reward_function(soll_temperatur, ist_temperatur, kosten, normalisierungsfaktor):
    temp_diff = soll_temperatur - ist_temperatur

    # Berechne die ursprüngliche Belohnung basierend auf der Temperaturdifferenz
    if temp_diff <= 0:
        reward = 1
    elif temp_diff <= 5:
        reward = 1 - (temp_diff / 5)
    elif temp_diff <= 10:
        reward = -((temp_diff - 5) / 5)
    else:
        reward = -1

    # Normalisiere die Kosten und ziehe sie von der Belohnung ab
    kosten_normalized = kosten / normalisierungsfaktor
    reward -= kosten_normalized

    # Stelle sicher, dass die Belohnung im Bereich von -1 bis +1 bleibt
    reward = max(-1, min(reward, 1))

    return reward        


# einfacher: Am Ende jeder Stunde 
# Delta Ist = Temp Soll - Temp Ist
# Delta Ist = max(Delta Ist, 0) soll nicht negativ werden
# Delta Max = das maximal akzeptierte Delta. Etwa 5 Grad
# Wenn Delta Ist > Delta Max, dann ist OP = Multiplikation ansonsten Division
# Wenn Betriebskosten <= 0, dann auf 0,1 setzen
# Reward = ( 1 -  ( Delta Ist / Delta Max )) OP Betriebskosten der Anlage der Stunde
# 