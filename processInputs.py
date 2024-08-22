import pandas as pd
import os
import sys
import json
from addInputs import addInputs

dir = os.getcwd()
run_path = sys.argv[1]

# For debugging
# scenario_name = 'with_ghp'
    
#################### PATH NAMES ####################

# Input path
data_path = run_path
if not os.path.exists(data_path):
    os.makedirs(data_path)
posts_path = os.path.join(data_path, 'inputs_all')

# Output path
outputs_path = run_path
if not os.path.exists(outputs_path):
    os.makedirs(outputs_path)

results_path = os.path.join(outputs_path, 'results', 'results_json')
if not os.path.exists(results_path):
    os.makedirs(results_path)

result_summary_path = os.path.join(outputs_path, 'results', 'results_summary')
if not os.path.exists(result_summary_path):
    os.makedirs(result_summary_path)

################### READ INPUTS ####################
(building_file,district_file,macrs_bonus_fraction,macrs_itc_reduction,federal_itc_fraction,utility_tarrif,
 om_cost_per_sqft_year,installed_cost_heatpump_per_ton,installed_cost_ghx_per_ft,
 installed_cost_building_hydronic_loop_per_sqft) = addInputs()

investment_scenario = pd.read_excel(os.path.join(data_path, building_file), sheet_name= "Timeseries")
building_ghp_data = pd.read_excel(os.path.join(data_path, building_file), sheet_name= "GHP",index_col=0)
district_ghx_data = pd.read_csv(os.path.join(data_path, district_file), index_col=0)

################### DISTRCIT IDS ###################
ghx_set = district_ghx_data.columns.to_list()
lon = district_ghx_data.loc[district_ghx_data.index=="lon",district_ghx_data.columns==ghx_set[0]].iloc[0,0]
lat = district_ghx_data.loc[district_ghx_data.index=="lat",district_ghx_data.columns==ghx_set[0]].iloc[0,0]

################### BUILDING IDS ###################
building_set = building_ghp_data.columns.to_list()
## Process inputs and save to REopt-format json files
# Building-level json file
for building_id in building_set:
    building = building_id.split("_", 1)[1]

    # Site info:
    post ={}
    post["Site"] = {}
    post["Site"]["latitude"] = lat
    post["Site"]["longitude"] = lon
    
    # Load input:
    building_elec_load_tot = investment_scenario['heating_electric_power_'+str(building)]/1000 + investment_scenario['pump_power_'+str(building)]/1000 + investment_scenario['ets_pump_power_'+str(building)]/1000
    investment_scenario['electric_load_tot_'+str(building)] = building_elec_load_tot
    building_elec_load = investment_scenario['electric_load_tot_'+str(building)]

    building_spaceheating_load = investment_scenario['electric_load_tot_'+str(building)]
    building_spaceheating_load = building_spaceheating_load*0.000003412/1000

    post["SpaceHeatingLoad"] = {}
    post["DomesticHotWaterLoad"] = {}
    post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load)
    post["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_spaceheating_load*0)

    post["ElectricLoad"] = {}
    post["ElectricLoad"]["loads_kw"] = list(building_elec_load)

    # Read individual building's utility tariff
    post["ElectricTariff"] = {}
    if os.path.exists(os.path.join(data_path,"utility_rates.csv")):
        r = pd.read_csv(os.path.join(data_path, "utility_rates.csv"), header=None)[0][0]
        post["ElectricTariff"]["urdb_label"] = r
    else:
        with open(os.path.join(data_path, utility_tarrif), 'rb') as handle:
            r = json.load(handle)
        post["ElectricTariff"]["urdb_response"] = r

    # Read GHP and GHX outputs:
    ghp_size = building_ghp_data.loc[building_ghp_data.index=="GHP_size_ton",building_ghp_data.columns==building_id].iloc[0,0]
    floor_area = building_ghp_data.loc[building_ghp_data.index=="floor_area_sqft",building_ghp_data.columns==building_id].iloc[0,0]
    fuel_cost_per_mmbtu = building_ghp_data.loc[building_ghp_data.index=="fuel_cost_per_mmbtu",building_ghp_data.columns==building_id].iloc[0,0]

    post["GHP"] = {}  
    post["GHP"]["require_ghp_purchase"] = 1
    post["GHP"]["building_sqft"] = floor_area
    post["GHP"]["om_cost_per_sqft_year"] = 0
    post["GHP"]["heatpump_capacity_sizing_factor_on_peak_load"] = 1.0

    post["ExistingBoiler"] = {}
    post["ExistingBoiler"]["fuel_cost_per_mmbtu"] = fuel_cost_per_mmbtu

    # ghpghx_responses:
    ghpghx_output = {}
    ghpghx_output["outputs"] = {}
    ghpghx_output["inputs"] = {}
    
    ghpghx_output["outputs"]["heat_pump_configuration"] = "WSHP"
    ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = [0] * 8760
    ghpghx_output["outputs"]["number_of_boreholes"] = 0 #number_of_boreholes
    ghpghx_output["outputs"]["length_boreholes_ft"] = 0 #length_of_boreholes
    ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = ghp_size
    ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = sum(building_elec_load)
    ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = list(building_elec_load)
    ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = list(building_elec_load)
    ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = [0] * 8760
    
    # Set all inputs = 0:
    ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = list(building_spaceheating_load)
    ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

    post["GHP"]["ghpghx_responses"] = [ghpghx_output]

    with open(os.path.join(posts_path, 'GHP_building_' + str(building) +'.json'), 'w') as handle:
        json.dump(post, handle)  
    
# District-level inputs:
for ghx_id in ghx_set:
    ghx = ghx_id.split("_", 1)[1]

    building_spaceheating_load = [0]*8760
    building_elec_load = [0]*8760

    post_dist ={}

    post_dist["SpaceHeatingLoad"] = {}
    post_dist["DomesticHotWaterLoad"] = {}
    post_dist["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = building_spaceheating_load
    post_dist["DomesticHotWaterLoad"]["fuel_loads_mmbtu_per_hour"] = building_spaceheating_load

    post_dist["Site"] = {}
    post_dist["Site"]["latitude"] = lat
    post_dist["Site"]["longitude"] = lon

    post_dist["ElectricLoad"] = {}
    post_dist["ElectricLoad"]["loads_kw"] = building_elec_load

    tarrif_file = "utility_rates.json"
    with open(os.path.join(data_path, tarrif_file), 'rb') as handle:
        r = json.load(handle)
    post_dist["ElectricTariff"] = {}    
    post_dist["ElectricTariff"]["urdb_response"] = r

    post_dist["ExistingBoiler"] = {}
    post_dist["ExistingBoiler"]["fuel_cost_per_mmbtu"] = fuel_cost_per_mmbtu

    # Read GHX sizes:
    number_of_boreholes = district_ghx_data.loc[district_ghx_data.index=="number_of_boreholes",district_ghx_data.columns==ghx_id].iloc[0,0]
    length_of_boreholes = district_ghx_data.loc[district_ghx_data.index=="length_of_boreholes",district_ghx_data.columns==ghx_id].iloc[0,0]

    ghpghx_output = {}
    ghpghx_output["outputs"] = {}
    ghpghx_output["inputs"] = {}

    ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = building_spaceheating_load
    ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

    ghx_pump_electric_con = investment_scenario["electrical_power_consumed_"+str(ghx)]
    ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = list(ghx_pump_electric_con)
    ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = 0
    ghpghx_output["outputs"]["number_of_boreholes"] = number_of_boreholes
    ghpghx_output["outputs"]["length_boreholes_ft"] = length_of_boreholes
    ghpghx_output["outputs"]["heat_pump_configuration"] = "WSHP"
    ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = sum(building_elec_load)*0
    ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = building_elec_load
    ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = building_elec_load
    ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = building_elec_load

    post_dist["GHP"] = {}  
    post_dist["GHP"]["require_ghp_purchase"] = 1
    post_dist["GHP"]["building_sqft"] = 0
    post_dist["GHP"]["om_cost_per_sqft_year"] = 0
    post_dist["GHP"]["heatpump_capacity_sizing_factor_on_peak_load"] = 1.0

    # Dispatch output:
    ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = building_elec_load
    ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = building_elec_load
    ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = building_elec_load

    ghpghx_output_all = [ghpghx_output, ghpghx_output]
    post_dist["GHP"]["ghpghx_responses"] = ghpghx_output_all

    with open(os.path.join(posts_path, 'GHX_' + str(ghx) + '.json'), 'w') as handle:
        json.dump(post_dist, handle)  