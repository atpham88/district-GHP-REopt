
def addInputs():
    ##################################################### 
    # Specify all your district GHP inputs in this file #
    #####################################################
    
    # 1. District inputs
    #####################################################
    district_file = 'GHP_scenario_district.csv'  # REQUIRED 
                                    # This file include GHX size (borehole #, length) and 
                                    # Site location (lon, lat) 

    # 2. Building inputs
    #####################################################
    building_file = 'GHP_scenario_building.xlsx'  # REQUIRED 
                                    # This file include timeseries of electric consumption, 
                                    # GHP size, floor area for each building

    # 3. Capital costs 
    # OPTIONAL, if not provided ('NA'), 
    # REopt default values will be used
    #####################################################
    installed_cost_heatpump_per_ton = 'NA'                  # GHP installation cost per ton
    installed_cost_ghx_per_ft = 'NA'                        # GHX installation cost per ft
    installed_cost_building_hydronic_loop_per_sqft = 'NA'   # Hydronic loop installation cost per sqft
    om_cost_per_sqft_year = 0                               # O&M cost

    # 4. Financials 
    # OPTIONAL, if not provided ('NA'), 
    # REopt default values will be used
    #####################################################
    macrs_bonus_fraction = 'NA'
    macrs_itc_reduction = 'NA'
    federal_itc_fraction = 'NA'


    # 6. Utility Tariff
    # REQUIRED, can use urdb label (string)
    # or own json file
    #####################################################
    utility_tarrif = "utility_rates.json"
    
    return (building_file,district_file,macrs_bonus_fraction,macrs_itc_reduction,federal_itc_fraction,utility_tarrif,
            om_cost_per_sqft_year,installed_cost_heatpump_per_ton,installed_cost_ghx_per_ft,
            installed_cost_building_hydronic_loop_per_sqft)

addInputs()                      