import pandas as pd
import numpy as np
import os
import glob
import sys
import json
from addInputs import addInputs
import matplotlib.pyplot as plt

dir = os.getcwd()
main_path = sys.argv[1]
scenario_name = sys.argv[2]
isBAU = int(sys.argv[3])

# For debugging
#scenario_name = 'GHP_standalone'
#main_path = "/Users/apham/Documents/Projects/REopt_Projects/FY25/URBANopt_REopt/5_building_site"
#isBAU = 0

run_path = os.path.join(main_path,scenario_name)

# Note: KWH_THERMAL_PER_TONHOUR = 3.51685
#     
#################### PATH NAMES ####################
# Input path
data_path = run_path
posts_path = os.path.join(data_path, 'inputs_all')
if not os.path.exists(posts_path):
    os.makedirs(posts_path)

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

files_posts = glob.glob(os.path.join(data_path, 'inputs_all/*'))
files_results = glob.glob(os.path.join(outputs_path, 'results', 'results_json/*'))

for f in files_posts:
    os.remove(f)
for f in files_results:
    os.remove(f)        

################### READ INPUTS ####################
(building_file,district_file,macrs_bonus_fraction,macrs_itc_reduction,federal_itc_fraction,
 offtaker_discount_rate_fraction,offtaker_tax_rate_fraction,om_cost_escalation_rate_fraction,
 elec_cost_escalation_rate_fraction,owner_discount_rate_fraction,owner_tax_rate_fraction,
 utility_tarrif,utility_rate,annual_energy_rate,utility_tarrif,om_cost_per_sqft_year,
 installed_cost_heatpump_per_ton,installed_cost_ghx_per_ft,installed_cost_building_hydronic_loop_per_sqft) = addInputs()

investment_scenario = pd.read_excel(os.path.join(data_path, building_file), sheet_name= "Timeseries")
building_ghp_data = pd.read_excel(os.path.join(data_path, building_file), sheet_name= "GHP",index_col=0)
district_ghx_data = pd.read_csv(os.path.join(data_path, district_file), index_col=0)

################### DISTRCIT IDS ###################
ghx_set = district_ghx_data.columns.to_list()
lon = district_ghx_data.loc[district_ghx_data.index=="lon",district_ghx_data.columns==ghx_set[0]].iloc[0,0]
lat = district_ghx_data.loc[district_ghx_data.index=="lat",district_ghx_data.columns==ghx_set[0]].iloc[0,0]
fuel_cost_per_mmbtu_dist = district_ghx_data.loc[district_ghx_data.index=="fuel_cost_per_mmbtu",district_ghx_data.columns==ghx_set[0]].iloc[0,0]

################### BUILDING IDS ###################
building_set = building_ghp_data.columns.to_list()
## Process inputs and save to REopt-format json files
# Building-level json file
if len(building_set) > 0:
    for building_id in building_set:
        building = building_id.split("_", 1)[1]

        # Site info:
        post ={}
        post["Site"] = {}
        post["Site"]["latitude"] = lat
        post["Site"]["longitude"] = lon
        
        # Building electric load:
        building_elec_load_tot = investment_scenario['heating_electric_power_'+str(building)]/1000 + investment_scenario['cooling_electric_power_'+str(building)]/1000 + investment_scenario['pump_power_'+str(building)]/1000 + investment_scenario['ets_pump_power_'+str(building)]/1000
        investment_scenario['electric_load_tot_'+str(building)] = building_elec_load_tot
        building_elec_load = investment_scenario['electric_load_tot_'+str(building)]

        # Plotting load profiles for each site
        fig, ax = plt.subplots(figsize=(9,6))
        plt.xlabel("Date",fontsize=14)
        plt.ylabel("Building Electricity Consumption (kW)", fontsize=14)
        if str(building) == "Restaurant":
            plt.ylim(0,25)
        elif str(building) == "Hotel":
            plt.ylim(0,180)
        elif str(building) == "Office":
            plt.ylim(0,360)
        elif str(building) == "Apartment":
            plt.ylim(0,40)
        elif str(building) == "Mall":
            plt.ylim(0,140)

        ax.plot(building_elec_load, color = 'skyblue', linewidth=0.5)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
        plt.xticks(np.linspace(0,8760,13), months)
        #if isBAU == 1:
        #    plt.ylim(0,180)
        plt.title("Electricity Consumption" + " - "+str(building),fontsize=14)
        fig_path = os.path.join(run_path, "figures")
        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        fig.savefig(os.path.join(fig_path, "electricity_consumption_building_"+str(building_id)+".png"),dpi=300,bbox_inches='tight', pad_inches=0.1)


        post["ElectricLoad"] = {}
        post["ElectricLoad"]["loads_kw"] = list(building_elec_load)
        post["ElectricLoad"]["year"] = 2025

        # Space heating load is not needed for URBANopt district GHP analysis but required for BAU analysis and for REopt's formatting purpose,
        # so, in case it's not needed set that to very small numbers close to 0
        post["SpaceHeatingLoad"] = {}

        if isBAU == 0:
            post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = [0.0000001] * 8760
        elif isBAU == 1:
            building_heating_load_tot = investment_scenario['heating_fuel_'+str(building)]/1000
            
            # Plotting heating load profiles for each site
            fig, ax = plt.subplots(figsize=(9,6))
            plt.xlabel("Date",fontsize=14)
            plt.ylabel("Building Fuel Consumption (MMBtu)", fontsize=14)
            #plt.ylim(0,3.5)
            #if building_id == 1252:
            #    plt.ylim(0,20)
            #elif building_id == 39593:
            #    plt.ylim(0,7.5)
            #elif building_id == 63944:
            #    plt.ylim(0,15)
            #elif building_id == 69264:
            #    plt.ylim(0,5)
            #elif building_id == 461703:
            #    plt.ylim(0,25)

            ax.plot(building_heating_load_tot, color = 'lightpink', linewidth=0.5)
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
            plt.xticks(np.linspace(0,8760,13), months)
            plt.title("Fuel Consumption" + " - "+str(building),fontsize=14)
            fig_path = os.path.join(run_path, "figures")
            if not os.path.exists(fig_path):
                os.makedirs(fig_path)
            fig.savefig(os.path.join(fig_path, "fuel_consumption_building_"+str(building_id)+".png"),dpi=300,bbox_inches='tight', pad_inches=0.1)

            post["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = list(building_heating_load_tot)

        # Utility tariff
        post["ElectricTariff"] = {}
        
        # If using flat energy rate:
        if utility_rate == 'flat':
            post["ElectricTariff"]["blended_annual_energy_rate"] = annual_energy_rate
        # If using urdb label:
        elif utility_rate == 'label':
            r = pd.read_csv(os.path.join(data_path, utility_tarrif), header=None)[0][0]
            post["ElectricTariff"]["urdb_label"] = r
        # if using monthly energy and demand rates (input the rates in utility_rates.csv):    
        elif utility_rate == 'monthly_rates':
            r = pd.read_csv(os.path.join(data_path, utility_tarrif))
            dfd = r.loc[r["Rate Type"] == "Demand"]
            dfe = r.loc[r['Rate Type'] == "Energy"]
            co = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            d = []
            e = []
            for c in co: 
                d.append(dfd[c].item())
                e.append(dfe[c].item())
            post['ElectricTariff']['monthly_energy_rates'] = e
            post['ElectricTariff']['monthly_demand_rates'] = d
        # If using customly built rate structure (saved as utility_rates.json):
        else:
            with open(os.path.join(data_path, utility_tarrif), 'rb') as handle:
                r = json.load(handle)
            post["ElectricTariff"]["urdb_response"] = r

        # Financial
        # If not defined in addInputs.py, use REopt's default values
        post["Financial"] = {} 
        if (offtaker_discount_rate_fraction != 'NA'):
            post["Financial"]["offtaker_discount_rate_fraction"] = offtaker_discount_rate_fraction      
        if (offtaker_tax_rate_fraction != 'NA'):
            post["Financial"]["offtaker_tax_rate_fraction"] = offtaker_tax_rate_fraction      
        if (om_cost_escalation_rate_fraction != 'NA'):
            post["Financial"]["om_cost_escalation_rate_fraction"] = om_cost_escalation_rate_fraction 
        if (owner_discount_rate_fraction != 'NA'):
            post["Financial"]["owner_discount_rate_fraction"] = owner_discount_rate_fraction 
        if (owner_tax_rate_fraction != 'NA'):
            post["Financial"]["owner_tax_rate_fraction"] = owner_tax_rate_fraction
        if (elec_cost_escalation_rate_fraction != 'NA'):
            post["Financial"]["elec_cost_escalation_rate_fraction"] = elec_cost_escalation_rate_fraction
            
        # Read GHP and GHX outputs:
        ghp_size = building_ghp_data.loc[building_ghp_data.index=="GHP_size_ton",building_ghp_data.columns==building_id].iloc[0,0]
        floor_area = building_ghp_data.loc[building_ghp_data.index=="floor_area_sqft",building_ghp_data.columns==building_id].iloc[0,0]
        fuel_cost_per_mmbtu = building_ghp_data.loc[building_ghp_data.index=="fuel_cost_per_mmbtu",building_ghp_data.columns==building_id].iloc[0,0]

        if isBAU == 0:
            post["GHP"] = {}  
            post["GHP"]["require_ghp_purchase"] = 1
            post["GHP"]["building_sqft"] = floor_area
            post["GHP"]["heatpump_capacity_sizing_factor_on_peak_load"] = 1.0

            # GHP/GHX capital & O&M costs:
            if om_cost_per_sqft_year != 'NA':
                post["GHP"]["om_cost_per_sqft_year"] = om_cost_per_sqft_year
            if installed_cost_heatpump_per_ton != 'NA':
                post["GHP"]["installed_cost_heatpump_per_ton"] = installed_cost_heatpump_per_ton
            if installed_cost_ghx_per_ft != 'NA':
                post["GHP"]["installed_cost_ghx_per_ft"] = installed_cost_ghx_per_ft
            if installed_cost_building_hydronic_loop_per_sqft != 'NA':
                post["GHP"]["installed_cost_building_hydronic_loop_per_sqft"] = installed_cost_building_hydronic_loop_per_sqft

            # GHP incentives:
            if (macrs_bonus_fraction != 'NA'):
                post["GHP"]["macrs_bonus_fraction"] = macrs_bonus_fraction
            if (macrs_itc_reduction != 'NA'):
                post["GHP"]["macrs_itc_reduction"] = macrs_itc_reduction
            if (federal_itc_fraction != 'NA'):
                post["GHP"]["federal_itc_fraction"] = federal_itc_fraction 

        # ExistingBoiler settings for BAU
        post["ExistingBoiler"] = {}
        post["ExistingBoiler"]["fuel_cost_per_mmbtu"] = fuel_cost_per_mmbtu
        post["ExistingBoiler"]["installed_cost_per_mmbtu_per_hour"] = 59920 

        # ghpghx_responses inputs (this is where all the URBANopt outputs go to)
        ghpghx_output = {}
        ghpghx_output["outputs"] = {}
        ghpghx_output["inputs"] = {}
        
        ghpghx_output["outputs"]["heat_pump_configuration"] = "WSHP"
        ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = [0] * 8760
        ghpghx_output["outputs"]["number_of_boreholes"] = 0 #number_of_boreholes (for individual buildings, this is 0)
        ghpghx_output["outputs"]["length_boreholes_ft"] = 0 #length_of_boreholes (for individual buildings, this is 0)
        ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = ghp_size
        ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = 0
        ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = [0] * 8760
        ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = [0] * 8760
        ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = [0] * 8760
        
        # Set all inputs = 0:
        ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = [0.0000001] * 8760
        ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

        if isBAU == 0:
            post["GHP"]["ghpghx_responses"] = [ghpghx_output]
        
        if isBAU == 0:
            with open(os.path.join(posts_path, scenario_name + '_building_' + str(building) +'.json'), 'w') as handle:
                json.dump(post, handle)
        elif isBAU == 1:
            with open(os.path.join(posts_path, scenario_name + '_building_' + str(building) +'.json'), 'w') as handle:
                json.dump(post, handle)
    
# District-level inputs:
if len(ghx_set) > 0: 
    for ghx_id in ghx_set:
        ghx = ghx_id.split("_", 1)[1]

        post_dist ={}
        
        # Site info:
        post_dist["Site"] = {}
        post_dist["Site"]["latitude"] = lat
        post_dist["Site"]["longitude"] = lon

        # GHX's electricity consumption:
        ghx_pump_electric_con = investment_scenario["electrical_power_consumed_"+str(ghx)]/1000
        
        # Plotting GHX electricity consumption
        fig, ax = plt.subplots(figsize=(9,6))
        plt.xlabel("Date",fontsize=14)
        plt.ylabel("GHX Electricity Consumption (kW)", fontsize=14)
        #if building_id == 1252:
        #    plt.ylim(0,20)
        #elif building_id == 39593:
        #    plt.ylim(0,7.5)
        #elif building_id == 63944:
        #    plt.ylim(0,15)
        #elif building_id == 69264:
        #    plt.ylim(0,5)
        #elif building_id == 461703:
        #    plt.ylim(0,25)
        ax.plot(ghx_pump_electric_con, color = 'skyblue', linewidth=0.5)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
        plt.xticks(np.linspace(0,8760,13), months)
        plt.title("Electricity Consumption" + " - GHX "+str(ghx),fontsize=14)
        fig_path = os.path.join(run_path, "figures")
        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        fig.savefig(os.path.join(fig_path, "electricity_consumption_ghx_"+str(ghx)+".png"))

        post_dist["ElectricLoad"] = {}
        post_dist["ElectricLoad"]["loads_kw"] = list(ghx_pump_electric_con)
        post_dist["ElectricLoad"]["year"] = 2025

        post_dist["SpaceHeatingLoad"] = {}
        post_dist["SpaceHeatingLoad"]["fuel_loads_mmbtu_per_hour"] = [0.00000001]*8760      # Is not used for URBANopt LCCA but must be > 0 to comply with REopt format

        # Electric tariff
        post_dist["ElectricTariff"] = {}
        # If using flat energy rate:
        if utility_rate == 'flat':
            post_dist["ElectricTariff"]["blended_annual_energy_rate"] = annual_energy_rate
        # If using urdb label:
        elif utility_rate == 'label':
            r = pd.read_csv(os.path.join(data_path, "utility_label.csv"), header=None)[0][0]
            post_dist["ElectricTariff"]["urdb_label"] = r
        # if using monthly energy and demand rates (input the rates in utility_rates.csv):    
        elif utility_rate == 'monthly_rates':
            r = pd.read_csv(os.path.join(data_path, "utility_rates.csv"))
            dfd = r.loc[r["Rate Type"] == "Demand"]
            dfe = r.loc[r['Rate Type'] == "Energy"]
            co = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            d = []
            e = []
            for c in co: 
                d.append(dfd[c].item())
                e.append(dfe[c].item())
            post_dist['ElectricTariff']['monthly_energy_rates'] = e
            post_dist['ElectricTariff']['monthly_demand_rates'] = d
        # If using customly built rate structure (saved as utility_rates.json):
        else:
            with open(os.path.join(data_path, utility_tarrif), 'rb') as handle:
                r = json.load(handle)
            post_dist["ElectricTariff"]["urdb_response"] = r

        # Financial
        # If not defined in addInputs.py, use REopt's default values
        post_dist["Financial"] = {} 
        if (offtaker_discount_rate_fraction != 'NA'):
            post_dist["Financial"]["offtaker_discount_rate_fraction"] = offtaker_discount_rate_fraction      
        if (offtaker_tax_rate_fraction != 'NA'):
            post_dist["Financial"]["offtaker_tax_rate_fraction"] = offtaker_tax_rate_fraction      
        if (om_cost_escalation_rate_fraction != 'NA'):
            post_dist["Financial"]["om_cost_escalation_rate_fraction"] = om_cost_escalation_rate_fraction 
        if (owner_discount_rate_fraction != 'NA'):
            post_dist["Financial"]["owner_discount_rate_fraction"] = owner_discount_rate_fraction 
        if (owner_tax_rate_fraction != 'NA'):
            post_dist["Financial"]["owner_tax_rate_fraction"] = owner_tax_rate_fraction
        if (elec_cost_escalation_rate_fraction != 'NA'):
            post_dist["Financial"]["elec_cost_escalation_rate_fraction"] = elec_cost_escalation_rate_fraction

        # Read GHX sizes:
        number_of_boreholes = district_ghx_data.loc[district_ghx_data.index=="number_of_boreholes",district_ghx_data.columns==ghx_id].iloc[0,0]
        length_of_boreholes = district_ghx_data.loc[district_ghx_data.index=="length_of_boreholes",district_ghx_data.columns==ghx_id].iloc[0,0]

        ghpghx_output = {}
        ghpghx_output["outputs"] = {}
        ghpghx_output["inputs"] = {}

        ghpghx_output["inputs"]["heating_thermal_load_mmbtu_per_hr"] = [0.0000001] * 8760
        ghpghx_output["inputs"]["cooling_thermal_load_ton"] = [0] * 8760

        ghpghx_output["outputs"]["yearly_ghx_pump_electric_consumption_series_kw"] = [0] * 8760
        ghpghx_output["outputs"]["peak_combined_heatpump_thermal_ton"] = 0.0000000001           # Must be > 0 for GHX capital cost to show up
        ghpghx_output["outputs"]["number_of_boreholes"] = number_of_boreholes
        ghpghx_output["outputs"]["length_boreholes_ft"] = length_of_boreholes
        ghpghx_output["outputs"]["heat_pump_configuration"] = "WSHP"
        ghpghx_output["outputs"]["yearly_total_electric_consumption_kwh"] = 0
        ghpghx_output["outputs"]["yearly_total_electric_consumption_series_kw"] = [0] * 8760
        ghpghx_output["outputs"]["yearly_heating_heatpump_electric_consumption_series_kw"] = [0] * 8760
        ghpghx_output["outputs"]["yearly_cooling_heatpump_electric_consumption_series_kw"] = [0] * 8760
        
        if isBAU == 0:
            post_dist["GHP"] = {}  
            post_dist["GHP"]["require_ghp_purchase"] = 1
            post_dist["GHP"]["building_sqft"] = 0
            post_dist["GHP"]["heatpump_capacity_sizing_factor_on_peak_load"] = 1.0
        
            # GHP/GHX capital & O&M costs:
            if om_cost_per_sqft_year != 'NA':
                post_dist["GHP"]["om_cost_per_sqft_year"] = om_cost_per_sqft_year
            if installed_cost_heatpump_per_ton != 'NA':
                post_dist["GHP"]["installed_cost_heatpump_per_ton"] = installed_cost_heatpump_per_ton
            if installed_cost_ghx_per_ft != 'NA':
                post_dist["GHP"]["installed_cost_ghx_per_ft"] = installed_cost_ghx_per_ft
            if installed_cost_building_hydronic_loop_per_sqft != 'NA':
                post_dist["GHP"]["installed_cost_building_hydronic_loop_per_sqft"] = installed_cost_building_hydronic_loop_per_sqft

            # GHP incentives:
            if (macrs_bonus_fraction != 'NA'):
                post_dist["GHP"]["macrs_bonus_fraction"] = macrs_bonus_fraction
            if (macrs_itc_reduction != 'NA'):
                post_dist["GHP"]["macrs_itc_reduction"] = macrs_itc_reduction
            if (federal_itc_fraction != 'NA'):
                post_dist["GHP"]["federal_itc_fraction"] = federal_itc_fraction 

        # ExistingBoiler settings for BAU
        post_dist["ExistingBoiler"] = {}
        post_dist["ExistingBoiler"]["fuel_cost_per_mmbtu"] = fuel_cost_per_mmbtu_dist
        post_dist["ExistingBoiler"]["installed_cost_per_mmbtu_per_hour"] = 56000 
 
        if isBAU == 0:
            post_dist["GHP"]["ghpghx_responses"] = [ghpghx_output]

        with open(os.path.join(posts_path, scenario_name + '_GHX_' + str(ghx) + '.json'), 'w') as handle:
            json.dump(post_dist, handle)  