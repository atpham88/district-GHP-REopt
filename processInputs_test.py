import pandas as pd
import os
import json

dir = os.getcwd()

#################### PATH NAMES ####################
posts_path = os.path.join(dir, 'data', 'inputs_test')
data_path = os.path.join(dir, 'data')

########## READ INPUTS (URBANopt OUTPUTS) ##########
ghp_scenario = pd.read_excel(os.path.join(data_path, "GHP_scenario.xlsx"), sheet_name= "Timeseries")
electric_load = pd.read_csv("/Users/apham/Documents/Projects/REopt_Projects/FY24/Geothermal/Model/district-GHP-REopt_old/data/buildings/building_1/electric_load.csv",header=None)
heating_load = pd.read_csv("/Users/apham/Documents/Projects/REopt_Projects/FY24/Geothermal/Model/district-GHP-REopt_old/data/buildings/building_1/heating_load.csv",header=None)

### District inputs:
## Shared GHX system
number_of_boreholes = 65
length_of_boreholes = 127.09

## Site info
# Location
lon = -105.2648427
lat = 39.99153232

# Building-level inputs:
# Site info:
post ={}
post["Site"] = {}
post["Site"]["latitude"] = lat
post["Site"]["longitude"] = lon

# Load input:
building_elec_load_tot = ghp_scenario['heating_electric_power_1']/1000 + ghp_scenario['pump_power_1']/1000 + ghp_scenario['pump_power_1']/1000
ghp_scenario['electric_load_tot_1'] = building_elec_load_tot
building_elec_load = ghp_scenario['electric_load_tot_1']
#building_elec_load = electric_load
ghx_pump_electric_con = ghp_scenario["electrical_power_consumed"]/1000

building_spaceheating_load = ghp_scenario['electric_load_tot_1']
building_spaceheating_load = building_spaceheating_load*0.000003412/1000
#building_spaceheating_load = heating_load

post["SpaceHeatingLoad"] = {}
post["DomesticHotWaterLoad"] = {}
post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load)
post["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load*0)
#post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load[0])
#post["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load[0]*0)

post["ElectricLoad"] = {}
post["ElectricLoad"]["loads_kw"] = list(building_elec_load)
#post["ElectricLoad"]["loads_kw"] = list(building_elec_load[0])

# Read individual building's utility tariff
tarrif_file = "utility_rates.json"
post["ElectricTariff"] = {}
with open(os.path.join(data_path, tarrif_file), 'rb') as handle:
    r = json.load(handle)
post["ElectricTariff"]["urdb_response"] = r

# Read GHP and GHX outputs:
ghp_size = 36
floor_area = 31623

post["GHP"] = {}  
post["GHP"]["require_ghp_purchase"] = 1
post["GHP"]["building_sqft"] = floor_area
#post["GHP"]["installed_cost_building_hydronic_loop_per_sqft"] = 1.7
#post["GHP"]["installed_cost_ghx_per_ft"] = 0
#post["GHP"]["installed_cost_heatpump_per_ton"] = 1075.0

post["ExistingBoiler"] = {}
post["ExistingBoiler"]["fuel_cost_per_mmbtu"] = 13.5

# ghpghx_responses:
#with open(os.path.join(data_path, "ghpghx_response.json"), 'rb') as handle:
#    ghpghx_output = json.load(handle)
ghpghx_output = {}
ghpghx_output["outputs"] = {}
ghpghx_output["inputs"] = {}

ghpghx_output["outputs"]["heat_pump_configuration"] = "WSHP"
ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = [0] * 8760
#ghpghx_output["outputs"]["yearly_heat_pump_eft_series_f"] = [0] * 8760
ghpghx_output["outputs"]["number_of_boreholes"] = number_of_boreholes
ghpghx_output["outputs"]["length_boreholes_ft"] = length_of_boreholes
ghpghx_output["outputs"]["peak_heating_heatpump_thermal_ton"] = ghp_size
ghpghx_output["outputs"]["peak_cooling_heatpump_thermal_ton"] = ghp_size
ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = ghp_size
ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = sum(building_elec_load)
ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load)
#ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = sum(building_elec_load[0])
#ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load[0])
ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)
ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)
#ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load[0])
#ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = list(building_elec_load[0]*0)

# Set all inputs = 0:
ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = list(building_spaceheating_load)
#ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = list(building_spaceheating_load[0])
ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

ghpghx_output_all = [ghpghx_output, ghpghx_output]
post["GHP"]["ghpghx_responses"] = ghpghx_output_all
post["GHP"]["heatpump_capacity_sizing_factor_on_peak_load"] = 1.0

#ghpghx_response ={}
#ghpghx_response["outputs"] = {}
#ghpghx_response["outputs"] = ghp_scenario["electrical_power_consumed"]

with open(os.path.join(posts_path, 'GHP_building_test.json'), 'w') as handle:
    json.dump(post, handle)  
    
