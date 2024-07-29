import pandas as pd
import os
import json

dir = os.getcwd()

#################### PATH NAMES ####################
posts_path = os.path.join(dir, 'data', 'inputs_all')
data_path = os.path.join(dir, 'data')

########## READ INPUTS (URBANopt OUTPUTS) ##########
bau_scenario = pd.read_csv(os.path.join(data_path, "BAU_scenario.csv"))
ghp_scenario = pd.read_excel(os.path.join(data_path, "GHP_scenario.xlsx"), sheet_name= "Timeseries")

### District inputs:
## Shared GHX system
number_of_boreholes = 65
length_of_boreholes = 127.09

## Site info
# Number of buildings
building_no = 2
building_set = [x+1 for x in list(range(building_no))]

# Location
lon = -105.2648427
lat = 39.99153232

# Building-level inputs:
for building in building_set:
    # Site info:
    post ={}
    post["Site"] = {}
    post["Site"]["latitude"] = lat
    post["Site"]["longitude"] = lon
    
    # Load input:
    building_elec_load_tot = ghp_scenario['heating_electric_power_'+str(building)]/1000 + ghp_scenario['pump_power_'+str(building)]/1000 + ghp_scenario['pump_power_'+str(building)]/1000
    ghp_scenario['electric_load_tot_'+str(building)] = building_elec_load_tot
    building_elec_load = ghp_scenario['electric_load_tot_'+str(building)]
    ghx_pump_electric_con = ghp_scenario["electrical_power_consumed"]/1000

    building_spaceheating_load = ghp_scenario['electric_load_tot_'+str(building)]
    building_spaceheating_load = building_spaceheating_load*0.000003412/1000

    post["SpaceHeatingLoad"] = {}
    post["DomesticHotWaterLoad"] = {}
    post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load)
    post["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load*0)

    post["ElectricLoad"] = {}
    post["ElectricLoad"]["loads_kw"] = list(building_elec_load)

    # Read individual building's utility tariff
    tarrif_file = "utility_rates.json"
    post["ElectricTariff"] = {}
    with open(os.path.join(data_path, tarrif_file), 'rb') as handle:
        r = json.load(handle)
    post["ElectricTariff"]["urdb_response"] = r

    # Read GHP and GHX outputs:
    if building == 1:
        ghp_size = 36
        floor_area = 31623
    elif building == 2:
        ghp_size = 1
        floor_area = 8804

    post["GHP"] = {}  
    post["GHP"]["require_ghp_purchase"] = 1
    post["GHP"]["building_sqft"] = floor_area
    post["GHP"]["om_cost_per_sqft_year"] = 0
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
    ghpghx_output["outputs"]["number_of_boreholes"] = 0 #number_of_boreholes
    ghpghx_output["outputs"]["length_boreholes_ft"] = 0 #length_of_boreholes
    #ghpghx_output["outputs"]["peak_heating_heatpump_thermal_ton"] = ghp_size
    #ghpghx_output["outputs"]["peak_cooling_heatpump_thermal_ton"] = ghp_size
    ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = ghp_size
    ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = sum(building_elec_load)
    ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load)
    ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load)
    ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = [0] * 8760
    
    # Set all inputs = 0:
    ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = list(building_spaceheating_load)
    ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

    ghpghx_output_all = [ghpghx_output, ghpghx_output]
    post["GHP"]["ghpghx_responses"] = ghpghx_output_all

    with open(os.path.join(posts_path, 'GHP_building_' + str(building) +'.json'), 'w') as handle:
        json.dump(post, handle)  
    
# District-level inputs:
building_spaceheating_load = ghp_scenario['electric_load_tot_'+str(building)]
building_spaceheating_load = building_spaceheating_load*0.000003412/1000

post_dist ={}

post_dist["SpaceHeatingLoad"] = {}
post_dist["DomesticHotWaterLoad"] = {}
post_dist["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load)
post_dist["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load*0)

post_dist["Site"] = {}
post_dist["Site"]["latitude"] = lat
post_dist["Site"]["longitude"] = lon

post_dist["ElectricLoad"] = {}
post_dist["ElectricLoad"]["loads_kw"] = list(building_elec_load)

tarrif_file = "utility_rates.json"
with open(os.path.join(data_path, tarrif_file), 'rb') as handle:
    r = json.load(handle)
post_dist["ElectricTariff"] = {}    
post_dist["ElectricTariff"]["urdb_response"] = r

post_dist["ExistingBoiler"] = {}
post_dist["ExistingBoiler"]["fuel_cost_per_mmbtu"] = 13.5

# Read GHX sizes:
#with open(os.path.join(data_path, "ghpghx_response.json"), 'rb') as handle:
#    ghpghx_output = json.load(handle)
ghpghx_output = {}
ghpghx_output["outputs"] = {}
ghpghx_output["inputs"] = {}

ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = list(building_spaceheating_load)
ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

ghx_pump_electric_con = ghp_scenario["electrical_power_consumed"]
ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = list(ghx_pump_electric_con)
ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = 0
ghpghx_output["outputs"]["number_of_boreholes"] = number_of_boreholes
ghpghx_output["outputs"]["length_boreholes_ft"] = length_of_boreholes
ghpghx_output["outputs"]["heat_pump_configuration"] = "WSHP"
ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = sum(building_elec_load)*0
ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load*0)
ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)
ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)

post_dist["GHP"] = {}  
post_dist["GHP"]["require_ghp_purchase"] = 1
post_dist["GHP"]["building_sqft"] = 0
post_dist["GHP"]["om_cost_per_sqft_year"] = 0
#post_dist["GHP"]["installed_cost_building_hydronic_loop_per_sqft"] = 1.7
#post_dist["GHP"]["installed_cost_ghx_per_ft"] = 14.0
#post_dist["GHP"]["installed_cost_heatpump_per_ton"] = 1075.0

# Dispatch output:
ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)
ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)
ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load*0)

ghpghx_output_all = [ghpghx_output, ghpghx_output]
post_dist["GHP"]["ghpghx_responses"] = ghpghx_output_all

with open(os.path.join(posts_path, 'GHP_district.json'), 'w') as handle:
    json.dump(post_dist, handle)  