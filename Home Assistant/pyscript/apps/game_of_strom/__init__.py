# config/pyscript/modules/ev_charging
from ev_charging.ev_charging_actions_ai import ev_charging_actions_ai
from ev_charging.ev_charging_actions_auto import ev_charging_actions_auto
from ev_charging.ev_charging_actions_user import ev_charging_actions_user
from ev_charging.ev_charging_controller import ev_charging_controller
from ev_charging.ev_charging_reward import ev_charging_reward

# config/pyscript/modules/space_heating
from space_heating.space_heating_actions_ai import space_heating_actions_ai
from space_heating.space_heating_actions_auto import space_heating_actions_auto
from space_heating.space_heating_actions_user import space_heating_actions_user
from space_heating.space_heating_controller import space_heating_controller
from space_heating.space_heating_controller import space_heating_hkr_controller
from space_heating.space_heating_reward import space_heating_reward

# config/pyscript/modules/water_heating
from water_heating.water_heating_actions_ai import water_heating_actions_ai
from water_heating.water_heating_actions_auto import water_heating_actions_auto
from water_heating.water_heating_actions_user import water_heating_actions_user
from water_heating.water_heating_controller import water_heating_controller
from water_heating.water_heating_reward import water_heating_reward

# config/pyscript/modules/energy_storage
from energy_storage.energy_storage_actions_ai import energy_storage_actions_ai
from energy_storage.energy_storage_actions_auto import energy_storage_actions_auto
from energy_storage.energy_storage_actions_user import energy_storage_actions_user
from energy_storage.energy_storage_controller import energy_storage_controller
from energy_storage.energy_storage_reward import energy_storage_reward
from energy_storage.energy_storage_manager import energy_storage_manager
from energy_storage.energy_storage_manager import set_kostal_battery_charge_power

# config/pyscript/modules/z_helper
from z_helper.calculate_battery_price import calculate_battery_price
from z_helper.calculate_costs import calculate_costs
from z_helper.persist_dwd import persist_dwd
from z_helper.persist_epex import persist_epex


############################################################################
# energy_storage
############################################################################    

# These defaults can be overwritten by input helper
input_select.energy_storage_actions = 'auto'
input_select.energy_storage_controller = 'on'
input_select.energy_storage_manager = 'on'

@state_active("input_select.energy_storage_actions == 'ai'")
@time_trigger("period(0:00, 5 min)")
def run_energy_storage_actions_ai():
    energy_storage_actions_ai()

@state_active("input_select.energy_storage_actions == 'auto'")
@time_trigger("period(0:00, 5 min)")
def run_energy_storage_actions_auto():
    energy_storage_actions_auto()

@state_active("input_select.energy_storage_actions == 'user'")
@time_trigger("period(0:00, 5 sec)")
def run_energy_storage_actions_user():
    energy_storage_actions_user(pyscript.app_config)

@state_active("input_select.energy_storage_controller == 'on'")
@time_trigger("period(0:00, 5 min)")
def run_energy_storage_controller():
    energy_storage_controller(pyscript.app_config)

@state_active("input_select.energy_storage_controller == 'off'")
@state_trigger("input_select.energy_storage_controller")
def deactivate_energy_storage_controller():
    log.warning("energy_storage_controller deactivated")    
    script.kostal_set_battery_min_soc(min_soc=5)

@time_trigger('cron(58 * * * *)')  # 2 Minuten vor jeder vollen Stunde
def run_energy_storage_reward():
    energy_storage_reward()

@state_active("input_select.energy_storage_manager == 'on'")
@time_trigger("period(0:00, 3 sec)")
def run_energy_storage_manager():
    energy_storage_manager()        

@state_active("input_select.energy_storage_manager == 'off'")
@state_trigger("input_select.energy_storage_manager")
def deactivate_energy_storage_manager():
    log.warning("energy_storage_manager deactivated")
    set_kostal_battery_charge_power(value=0)
    

############################################################################
# ev_charging
############################################################################

# These defaults can be overwritten by input helper
input_select.ev_charging_actions = 'auto'
input_select.ev_charging_controller = 'on'


@state_active("input_select.ev_charging_actions == 'ai'")
@time_trigger("period(0:00, 5 min)")
def run_ev_charging_actions_ai():
    ev_charging_actions_ai()

@state_active("input_select.ev_charging_actions == 'auto'")
@time_trigger("period(0:00, 5 min)")
def run_ev_charging_actions_auto():
    ev_charging_actions_auto()

@state_active("input_select.ev_charging_actions == 'user'")
@time_trigger("period(0:00, 5 sec)")
def run_ev_charging_actions_user():
    ev_charging_actions_user(pyscript.app_config)

@state_active("input_select.ev_charging_controller == 'on'")
@time_trigger("period(0:00, 5 min)")
def run_ev_charging_controller():
    ev_charging_controller(pyscript.app_config)

@state_active("input_select.ev_charging_controller == 'off'")
@state_trigger("input_select.ev_charging_controller")
def deactivate_ev_charging_controller():
    log.warning("ev_charging_controller deactivated")
    # Beim Ausstellen des Controllers Beladung beenden
    script.goe_set_ampere(ampere=6)
    script.goe_set_phase(phase="1: 1-Phasig")    
    script.goe_set_state(state="1: Off")        

@time_trigger('cron(58 * * * *)')  # 2 Minuten vor jeder vollen Stunde
def run_ev_charging_reward():
    ev_charging_reward()    


############################################################################
# space_heating
############################################################################

# These defaults can be overwritten by input helper
input_select.space_heating_actions = 'auto'
input_select.space_heating_controller = 'on'

@state_active("input_select.space_heating_actions == 'ai'")
@time_trigger("period(0:00, 5 min)")
def run_space_heating_actions_ai():
    space_heating_actions_ai()

@state_active("input_select.space_heating_actions == 'auto'")
@time_trigger("period(0:00, 5 min)")
def run_space_heating_actions_auto():
    space_heating_actions_auto()

@state_active("input_select.space_heating_actions == 'user'")
@time_trigger("period(0:00, 5 sec)")
def run_space_heating_actions_user():
    space_heating_actions_user(pyscript.app_config)

@state_active("input_select.space_heating_controller == 'on'")
@time_trigger("period(0:00, 5 min)")
def run_space_heating_controller():
    space_heating_controller(pyscript.app_config)
    space_heating_hkr_controller()

@state_active("input_select.space_heating_controller == 'off'")
@state_trigger("input_select.space_heating_controller")
def deactivate_space_heating_controller():
    log.warning("space_heating_controller deactivated")    
    # Beim Ausstellen des Controllers Festwertbetrieb ausstellen
    # Dann übernimmt wieder Programmbetrieb der WP
    script.isg_set_festwertbetrieb_ausstellen(aus_wert="AUS")
    script.hkr_set_temperature(temperature=21)

@time_trigger('cron(58 * * * *)')  # 2 Minuten vor jeder vollen Stunde
def run_space_heating_reward():
    space_heating_reward()    


############################################################################
# water_heating
############################################################################

input_select.water_heating_actions = 'auto'
input_select.water_heating_controller = 'on'

@state_active("input_select.water_heating_actions == 'ai'")
@time_trigger("period(0:00, 5 min)")
def run_water_heating_actions_ai():
    water_heating_actions_ai()

@state_active("input_select.water_heating_actions == 'auto'")
@time_trigger("period(0:00, 5 min)")
def run_water_heating_actions_auto():
    water_heating_actions_auto()

@state_active("input_select.water_heating_actions == 'user'")
@time_trigger("period(0:00, 5 sec)")
def run_water_heating_actions_user():
    water_heating_actions_user(pyscript.app_config)

@state_active("input_select.water_heating_controller == 'on'")
@time_trigger("period(0:00, 5 min)")
def run_water_heating_controller():
    water_heating_controller(pyscript.app_config)

@state_active("input_select.water_heating_controller == 'off'")
@state_trigger("input_select.water_heating_controller")
def deactivate_water_heating_controller():
    log.warning("water_heating_controller deactivated")    
    # Beim Ausstellen des Controllers Temperatur festlegen
    script.isg_set_komfort_temperatur_warmwasser(komforttemperatur_warmwasser=50)   

@time_trigger('cron(58 * * * *)')  # 2 Minuten vor jeder vollen Stunde
def run_water_heating_reward():
    water_heating_reward()    


############################################################################
# helper
############################################################################

@time_trigger('cron(57 * * * *)')  # 3 Minuten vor jeder vollen Stunde
def run_calculate_battery_price():
    calculate_battery_price()

@time_trigger('cron(58 * * * *)')  # 2 Minuten vor jeder vollen Stunde
def run_calculate_costs():
    calculate_costs()

@state_trigger("sensor.hohenholte_sonnenscheindauer")
@state_trigger("sensor.hohenholte_sonneneinstrahlung")
@state_trigger("sensor.hohenholte_temperatur")
def run_persist_dwd():
    persist_dwd(pyscript.app_config)   

@state_trigger("sensor.epex_spot_de_lu_price")
def run_persist_epex():
    persist_epex(pyscript.app_config)