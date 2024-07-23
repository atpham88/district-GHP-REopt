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

### Process buildings inputs
## Site info

# Number of buildings:
building_no = 2
building_set = [x+1 for x in list(range(building_no))]

# Location:
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
    building_elec_load_tot = ghp_scenario['heating_electric_power_'+str(building)] + ghp_scenario['pump_power_'+str(building)] + ghp_scenario['pump_power_'+str(building)]
    ghp_scenario['electric_load_tot_'+str(building)] = building_elec_load_tot
    building_elec_load = ghp_scenario['electric_load_tot_'+str(building)]

    building_ghp_output_kw = ghp_scenario['heating_electric_power_'+str(building)]*ghp_scenario['cop_'+str(building)]
    building_ghp_output = building_ghp_output_kw*0.003412/1000 # in ton

    building_spaceheating_load = ghp_scenario['electric_load_tot_'+str(building)]*0
    building_spaceheating_load = building_spaceheating_load*0.003412/1000

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

    # Read GHP and GHX sizes:
    # GHP and floor area:
    if building == 1:
        ghp_size = 36
        floor_area = 31623
    elif building == 2:
        ghp_size = 1
        floor_area = 8804

    post["GHP"] = {}  
    post["GHP"]["building_sqft"] = floor_area

    post["ExistingBoiler"] = {}
    post["ExistingBoiler"]["fuel_cost_per_mmbtu"] = 13.5

    # GHX:
    with open(os.path.join(data_path, "ghpghx_response.json"), 'rb') as handle:
        ghpghx_output = json.load(handle)

    number_of_boreholes = 65
    length_of_boreholes = 127.09
    ghx_pump_electric_con = ghp_scenario["electrical_power_consumed"]
    ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = list(ghx_pump_electric_con)
    ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = ghp_size
    ghpghx_output["outputs"]["number_of_boreholes"] = number_of_boreholes
    ghpghx_output["outputs"]["length_boreholes_ft"] = length_of_boreholes

    # Dispatch output:
    ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load)
    ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = list(building_elec_load*0)
    ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load)

    ghpghx_output = [ghpghx_output, ghpghx_output]
    post["GHP"]["ghpghx_responses"] = ghpghx_output

    #ghpghx_response ={}
    #ghpghx_response["outputs"] = {}
    #ghpghx_response["outputs"] = ghp_scenario["electrical_power_consumed"]

    with open(os.path.join(posts_path, 'GHP_building_' + str(building) +'.json'), 'w') as handle:
        json.dump(post, handle)  
    

