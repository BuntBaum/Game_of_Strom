
def calculate_battery_price():

    # Nach HA Neustart ist Sensor nicht mehr da
    # returns all HASS state variable (entity) names
    entities = state.names(domain=None)    
    if "sensor.kostal_plenticore_battery_price_per_kwh" not in entities:
        # Sensor initialisieren
        sensor.kostal_plenticore_battery_price_per_kwh = 0
    
    # Sensoren einlesen
    pv_load = float(sensor.kostal_plenticore_battery_charge_from_pv_hourly) # Batterie-Beladung aus PV in kWh je Stunde
    grid_load = float(sensor.kostal_plenticore_battery_charge_from_grid_hourly) # Batterie-Beladung aus Netz in kWh je Stunde
    grid_price = float(sensor.epex_spot_de_lu_price.price_ct_per_kwh) / 100 # Netzstrompreis je Stunde je kWh in Euro
    battery_price = float(sensor.kostal_plenticore_battery_price_per_kwh) # Strompreis der Batterie je Stunde je kWh in Euro    
    
    # Wie viel Energie ist derzeit im Speicher?
    battery_work_capacity = 5760 - 760 # kWh minus Abzug da Min SOC und Kapazitätsverlust über die Zeit
    battery_soc = float(sensor.scb_battery_soc)
    battery_energy = battery_soc * battery_work_capacity

    # Berechnung der Kosten der bereits in der Batterie gespeicherten Energie
    stored_energy_cost = battery_energy * battery_price

    # Gesamtmenge an geladener Energie in dieser Stunde
    total_load = pv_load + grid_load

    # Effektive Menge an geladener Energie unter Berücksichtigung der Batterieeffizienz
    battery_efficiency = 1.0  
    effective_load = total_load * battery_efficiency

    # Kosten für die Energie aus dem Netz
    grid_cost = grid_load * grid_price

    # Kosten für die Energie aus der PV
    pv_price = 0.08 # €/kWh entgangene Einspeisevergütung
    pv_cost = pv_load * pv_price

    # Gesamtkosten für die geladene Energie
    total_cost = grid_cost + pv_cost  # wobei die PV-Energie nichts kostet

    # Gesamte Energie und Gesamtkosten nach dem Laden
    total_energy_after_charging = battery_energy + effective_load
    total_cost_after_charging = stored_energy_cost + total_cost

    # Kosten pro kWh nach dem Laden
    price_per_kwh_after_charging = total_cost_after_charging / total_energy_after_charging if total_energy_after_charging > 0 else 0

    # Ergebnis im Sensor speichern
    sensor.kostal_plenticore_battery_price_per_kwh = str(price_per_kwh_after_charging)
    sensor.kostal_plenticore_battery_price_per_kwh.unit_of_measurement = "EUR"
    sensor.kostal_plenticore_battery_price_per_kwh.friendly_name = "Kostal Plenticore Battery Price per kWh"
    sensor.kostal_plenticore_battery_price_per_kwh.herkunft = "custom_components.pyscript.apps.batterie_strompreis_berechnen"
    sensor.kostal_plenticore_battery_price_per_kwh.kosten_aktuelle_beladung_euro = str(total_cost)
    sensor.kostal_plenticore_battery_price_per_kwh.kosten_enthaltene_ladung_euro = str(total_cost_after_charging)

