
def calculate_costs():


    # Ziel der Funktion: Die Stromkosten je Stunde für Wärmepumpe, Elektroauto, usw. berechnen und speichern

    # Nach HA Neustart ist Sensor nicht mehr da
    # returns all HASS state variable (entity) names
    entities = state.names(domain=None)    
    if "sensor.kostal_plenticore_battery_price_per_kwh" not in entities:
        # Sensor initialisieren
        sensor.kostal_plenticore_battery_price_per_kwh = 0    

    # Energieverbrauch beschaffen
    hourly_consumption_home = float(sensor.kostal_plenticore_home_consumption_total_hourly)
    hourly_consumption_home_from_pv = float(sensor.kostal_plenticore_home_consumption_from_pv_hourly)
    hourly_consumption_home_from_grid = float(sensor.kostal_plenticore_home_consumption_from_grid_hourly)
    hourly_consumption_home_from_battery = float(sensor.kostal_plenticore_home_consumption_from_battery_hourly)

    hourly_consumption_heat = float(sensor.isg_vd_heizen_leistungsaufnahme_stundlich)
    hourly_consumption_water = float(sensor.isg_vd_wasser_leistungsaufnahme_stundlich)
    hourly_consumption_car = 0 # float(sensor.zoe_charged_energy_hourly) #TODO

    # Preise beschaffen
    price_euro_per_kwh_from_grid =  float(sensor.epex_spot_de_lu_price.price_ct_per_kwh) / 100
    price_euro_per_kwh_from_pv =  0.08 # da entgangene Einspeisevergütung
    price_euro_per_kwh_from_battery =  float(sensor.kostal_plenticore_battery_price_per_kwh)

    # Welche Quellen decken den Energieverbrauch?
    if hourly_consumption_home > 0:
        rate_pv = hourly_consumption_home_from_pv / hourly_consumption_home
        rate_grid = hourly_consumption_home_from_grid / hourly_consumption_home
        rate_battery = hourly_consumption_home_from_battery / hourly_consumption_home
    else:
        rate_pv = 0
        rate_grid = 0
        rate_battery = 0

    # Den Verbrauch nach Energiequellen aufteilen - Heizung
    hourly_consumption_heat_from_pv = hourly_consumption_heat * rate_pv
    hourly_consumption_heat_from_grid = hourly_consumption_heat * rate_grid
    hourly_consumption_heat_from_battery = hourly_consumption_heat * rate_battery

    # Den Verbrauch nach Energiequellen aufteilen - Warmwasser
    hourly_consumption_water_from_pv = hourly_consumption_water * rate_pv
    hourly_consumption_water_from_grid = hourly_consumption_water * rate_grid
    hourly_consumption_water_from_battery = hourly_consumption_water * rate_battery

    # Den Verbrauch nach Energiequellen aufteilen - Elektroauto
    hourly_consumption_car_from_pv = hourly_consumption_car * rate_pv
    hourly_consumption_car_from_grid = hourly_consumption_car * rate_grid
    hourly_consumption_car_from_battery = hourly_consumption_car * rate_battery

    # Kosten berechnen - Heizen
    hourly_cost_heat_from_pv = hourly_consumption_heat_from_pv * price_euro_per_kwh_from_pv
    hourly_cost_heat_from_grid = hourly_consumption_heat_from_grid * price_euro_per_kwh_from_grid
    hourly_cost_heat_from_battery = hourly_consumption_heat_from_battery * price_euro_per_kwh_from_battery
    hourly_cost_heat = hourly_cost_heat_from_pv + hourly_cost_heat_from_grid + hourly_cost_heat_from_battery

    # Kosten berechnen - Warmwasser
    hourly_cost_water_from_pv = hourly_consumption_water_from_pv * price_euro_per_kwh_from_pv
    hourly_cost_water_from_grid = hourly_consumption_water_from_grid * price_euro_per_kwh_from_grid
    hourly_cost_water_from_battery = hourly_consumption_water_from_battery * price_euro_per_kwh_from_battery
    hourly_cost_water = hourly_cost_water_from_pv + hourly_cost_water_from_grid + hourly_cost_water_from_battery

    # Kosten berechnen - Elektroauto
    hourly_cost_car_from_pv = hourly_consumption_car_from_pv * price_euro_per_kwh_from_pv
    hourly_cost_car_from_grid = hourly_consumption_car_from_grid * price_euro_per_kwh_from_grid
    hourly_cost_car_from_battery = hourly_consumption_car_from_battery * price_euro_per_kwh_from_battery
    hourly_cost_car = hourly_cost_car_from_pv + hourly_cost_car_from_grid + hourly_cost_car_from_battery

    # Kosten berechnen - Haushalt
    hourly_cost_home_from_pv = hourly_consumption_home_from_pv * price_euro_per_kwh_from_pv
    hourly_cost_home_from_grid = hourly_consumption_home_from_grid * price_euro_per_kwh_from_grid
    hourly_cost_home_from_battery = hourly_consumption_home_from_battery * price_euro_per_kwh_from_battery
    hourly_cost_home = hourly_cost_home_from_pv + hourly_cost_home_from_grid + hourly_cost_home_from_battery

    # Kosten speichern - Heizen
    # TODO

    # Kosten speichern - Elektroauto
    # TODO    

    # Kosten speichern - Haushalt
    # TODO    

    # Kosten speichern - Warmwasser
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich = str(hourly_cost_water)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.unit_of_measurement = "EUR"
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.friendly_name = "ISG VD Wasser Leistungsaufnahme Kosten stündlich"
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.herkunft = "custom_components.pyscript.apps.stromkosten_berechnen"
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_cost_water_from_pv = str(hourly_cost_water_from_pv)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_cost_water_from_grid = str(hourly_cost_water_from_grid)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_cost_water_from_battery = str(hourly_cost_water_from_battery)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_consumption_water_from_pv = str(hourly_consumption_water_from_pv)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_consumption_water_from_grid = str(hourly_consumption_water_from_grid)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_consumption_water_from_battery = str(hourly_consumption_water_from_battery)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.hourly_consumption_water = str(hourly_consumption_water)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.price_euro_per_kwh_from_pv = str(price_euro_per_kwh_from_pv)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.price_euro_per_kwh_from_grid = str(price_euro_per_kwh_from_grid)
    sensor.isg_vd_wasser_leistungsaufnahme_kosten_stundlich.price_euro_per_kwh_from_battery = str(price_euro_per_kwh_from_battery)

