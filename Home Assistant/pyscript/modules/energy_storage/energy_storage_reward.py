
def energy_storage_reward():
    log.info("kostal_battery_reward:")
    
    # Nach HA Neustart ist Sensor nicht mehr da
    # returns all HASS state variable (entity) names
    entities = state.names(domain=None)    
    if "sensor.kostal_plenticore_battery_reward" not in entities:
        # Sensor initialisieren
        sensor.kostal_plenticore_battery_reward = 0


    # Energie
    battery_from_grid = float(sensor.kostal_plenticore_battery_charge_from_grid_hourly) # Batterie-Beladung aus Netz in kWh je Stunde
    battery_from_pv = float(sensor.kostal_plenticore_battery_charge_from_pv_hourly) # Batterie-Beladung aus PV in kWh je Stunde
    battery_to_home = float(sensor.kostal_plenticore_home_consumption_from_battery_hourly) # Entladung aus Batterie in kWh je Stunde
    max_energy = 2.7 # je Stunde können maximal 2.7 kWh aus der Batterie geladen oder entladen werden
    
    # Preise
    grid_price = float(sensor.epex_spot_de_lu_price.price_ct_per_kwh) / 100 # Netzstrompreis je Stunde je kWh in Euro
    grid_price_min = float(sensor.epex_spot_de_lu_lowest_price.price_ct_per_kwh) / 100 # Minimaler Netzstrompreis je Stunde je kWh in Euro    
    grid_price_avg = float(sensor.epex_spot_de_lu_average_price.price_ct_per_kwh) / 100 # Durchschnittlicher Netzstrompreis je Stunde je kWh in Euro
    battery_price = float(sensor.kostal_plenticore_battery_price_per_kwh) # Strompreis der Batterie je Stunde je kWh in Euro  


    # PV Reward
    # Wie viel Energie konnte aus der PV in die Batterie geladen werden im Vergleich zur maximal möglichen Befüllung?
    reward_charge_from_pv = get_reward( paid_price=0,
                                        reference_price=1,
                                        min_price=0,
                                        energy=battery_from_pv,
                                        max_energy=max_energy)
    
    # Grid Reward
    # Was hat es gekostet die Batterie jetzt aus dem Netz zu befüllen im Vergleich zum Tagesdurchschnitt?
    reward_charge_from_grid = get_reward(   paid_price=grid_price,
                                            reference_price=grid_price_avg,
                                            min_price=grid_price_min,
                                            energy=battery_from_grid,
                                            max_energy=max_energy)

    # Consumption Reward
    # Was hat es gekostet die Energie aus der Batterie zu nutzen im Vergleich zu den aktuellen Netzpreisen?
    reward_discharge_to_home = get_reward(  paid_price=battery_price,
                                            reference_price=grid_price,
                                            min_price=grid_price_min,
                                            energy=battery_to_home,
                                            max_energy=max_energy)


    # Gesamt Reward für Battery
    battery_reward = reward_charge_from_pv + reward_charge_from_grid + reward_discharge_to_home


    # Ergebnis im Sensor speichern
    sensor.kostal_plenticore_battery_reward = battery_reward
    sensor.kostal_plenticore_battery_reward.reward_discharge_to_home = reward_discharge_to_home
    sensor.kostal_plenticore_battery_reward.reward_charge_from_pv = reward_charge_from_pv
    sensor.kostal_plenticore_battery_reward.reward_charge_from_grid = reward_charge_from_grid
    sensor.kostal_plenticore_battery_reward.friendly_name = "Kostal Plenticore Battery Reward"
    sensor.kostal_plenticore_battery_reward.herkunft = "custom_components.pyscript.apps.kostal_battery_reward"
    sensor.kostal_plenticore_battery_reward.unit_of_measurement = "state"





def get_reward(paid_price, reference_price, min_price, energy, max_energy):
    
    # Wie viel wurde tatsächlich eingespart?
    price_difference = reference_price - paid_price
    
    # Wie viel hätte maximal eingespart werden können?
    max_price_difference = reference_price - min_price

    if max_price_difference == 0:
        max_price_difference = 0.00001

    # Normalize the price difference to the range of [0, 1]
    reward = price_difference / max_price_difference

    # Make sure the reward stays in the range of [-1, 1]
    reward = max(min(reward, 1), -1)

    # Now consider the loaded energy
    reward *= energy / max_energy  # assuming that the max loadable energy is 2.7kWh

    return reward    