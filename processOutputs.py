import pandas as pd
import numpy as np
import os
import json
from datetime import date

dir = os.getcwd()

### PATH NAMES ### 
results_path = os.path.join(dir, 'results', 'results_json')
result_summary_path = os.path.join(dir, 'results','results_summary')

# Add all column headers for output CSV file here (MUST align with order or results added in SaveOutputs)
colHeaders_types = {
    # Main Results
    "ID": str,
    #"LCC BAU [$]": float,
    "LCC [$]": float,
    #"NPV [$]": float,
    #"Analysis Period Elec Cost Savings [%]": float,
    "lifecycle capital costs": float,

    ## LCC Breakdown
    "lifecycle_om_costs_after_tax": float,
    "lifecycle_capital_costs_plus_om_after_tax": float,
    "lifecycle_elecbill_after_tax": float,
    "lifecycle_emissions_cost_climate": float,
    "REopt Solver Seconds": float,

    #"Simple Payback [years]": float,
    "Initial Capital Costs After Incentives [$]": float,
    
    "Annual Load [kWh]": float,
 
    #"Year One Bill_BAU [$]": float,
    "Year One Bill [$]": float,
    #"Year One Bill Savings [$]": float,

    #"Analysis Period Emissions_BAU [tonnes CO2]": float,
    "Analysis Period Emissions [tonnes CO2]": float,
    #"Analysis Period Emissions Savings [tonnes CO2]": float,
    #"Analysis Period Emissions Savings [%]": float,
    #"Analysis Period Emissions Savings [%] - Check": float,
    #"Annual Emissions_BAU [tonnes CO2]": float,
    "Annual Emissions [tonnes CO2]": float,
    #"Annual Emissions Savings [tonnes CO2]": float,
    "Health Damage Costs [$]": float
    
}
colHeaders = [i for i in colHeaders_types.keys()]

# Functions:
def SaveOutputs(res, name, colHeaders):
    building = name.split(".", 1)[0]

    # Get saved response
    with open(os.path.join(results_path, name), 'rb') as handle:
        r = json.load(handle)

    # Update results array
    tariff = r["ElectricTariff"]
    site = r["Site"]
    fin = r["Financial"]

    #capital costs
    res = np.append(res, building) # Building Name
    #res = np.append(res, r["Financial"]["lcc_bau"])  # "Analysis Period Elec Costs_BAU [$]", 
    res = np.append(res, r["Financial"]["lcc"])    # "Analysis Period Elec Costs_OPTIMIZED [$]",           
    #res = np.append(res, r["Financial"]["npv"])    # NPV,
    #res = np.append(res, ((r["Financial"]["npv"])/(r["Financial"]["lcc_bau"]))*100) # "Analysis Period Elec Cost Savings [%]"
    res = np.append(res, fin["lifecycle_capital_costs"]) #  "lifecycle_generation_tech_capital_costs",
    res = np.append(res, fin["lifecycle_om_costs_after_tax"]) #  "lifecycle_om_costs_after_tax",
    res = np.append(res, fin["lifecycle_capital_costs_plus_om_after_tax"]) # "lifecycle_capital_costs_plus_om_after_tax"
    res = np.append(res, fin["lifecycle_elecbill_after_tax"]) #  "lifecycle_elecbill_after_tax",
    res = np.append(res, fin["lifecycle_emissions_cost_climate"]) #  "lifecycle_emissions_cost_climate"
    res = np.append(res, r["solver_seconds"])    # "REopt Solver Seconds"

    #res = np.append(res, r["Financial"]["simple_payback_years"]) # "Simple Payback [years]",
    res = np.append(res, r["Financial"]["initial_capital_costs_after_incentives"]) #capital costs

    res = np.append(res, np.sum(r["ElectricLoad"]["load_series_kw"]))  # "Annual Load [kWh]"

    #res = np.append(res, tariff["year_one_bill_before_tax_bau"])   # "Year One Bill [$]",
    res = np.append(res, tariff["year_one_bill_before_tax"])    # "Year One Bill [$]",
    #tot_sav = tariff["year_one_bill_before_tax_bau"]-tariff["year_one_bill_before_tax"]
    #res = np.append(res, tot_sav)    # "Year One Bill Savings [$]",

    #res = np.append(res, site["lifecycle_emissions_tonnes_CO2_bau"])    # "Analysis Period Emissions_BAU [tonnes CO2]",
    res = np.append(res, site["lifecycle_emissions_tonnes_CO2"])    # "Analysis Period Emissions[tonnes CO2]",
    #res = np.append(res, site["lifecycle_emissions_tonnes_CO2_bau"]-site["lifecycle_emissions_tonnes_CO2"])    # "Analysis Period Emissions Savings [tonnes CO2]",
    #res = np.append(res, (site["lifecycle_emissions_tonnes_CO2_bau"]-site["lifecycle_emissions_tonnes_CO2"])/site["lifecycle_emissions_tonnes_CO2_bau"]*100)    # "Analysis Period Emissions Savings [%]",
    #res = np.append(res, site["lifecycle_emissions_reduction_CO2_fraction"])  # "Analysis Period Emissions Savings [%] - Check"
    #res = np.append(res, site["annual_emissions_tonnes_CO2_bau"])    # "Year One Emissions_BAU [tonnes CO2]",
    res = np.append(res, site["annual_emissions_tonnes_CO2"])    # "Year One Emissions [tonnes CO2]",
    #res = np.append(res, site["annual_emissions_tonnes_CO2_bau"]-site["annual_emissions_tonnes_CO2"])    # "Year One Emissions Savings [tonnes CO2]",
    #res = np.append(res, r["Financial"]["lifecycle_emissions_cost_health_bau"]-r["Financial"]["lifecycle_emissions_cost_health"]) # "Avoided Health Damage Costs [$]"
    res = np.append(res, r["Financial"]["lifecycle_emissions_cost_health"]) # "Health Damage Costs [$]"
            
    return res

files = os.listdir(results_path)
res = np.array([])
count = 0
for name in files:
    if name == ".DS_Store":
        continue
    if "json" in name: # to exclude random hidden files
        res = SaveOutputs(res, name, colHeaders)
        count+=1

        df = pd.DataFrame(np.reshape(res,(count,len(colHeaders))), columns= colHeaders) #, index = LPs.columns[0:ub])
        cols = df.columns
        cols = cols.insert(4,cols[-1])
        cols = cols[:-1]
        df = df[cols]

    for col, col_type in colHeaders_types.items():
        df[col] = df[col].astype(col_type)
    
    df.round(3).to_csv("{}/{}_results_summary.csv".format(result_summary_path, date.today()))
    df.round(3).to_csv(os.path.join(dir, "results", "results_summary", "results_summary.csv"))



