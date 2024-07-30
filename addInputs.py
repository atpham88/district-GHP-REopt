
def addInputs():
    ##################################################### 
    # Specify all your district GHP inputs in this file #
    #####################################################
    
    # 1. District inputs
    #####################################################
    # Site                      
    lon = -105.2648427              # REQUIRED
    lat = 39.99153232               # REQUIRED
    buildings_id = ['1','2']        # REQUIRED (building id should match the ones in URBANopt results file)

    # GHX
    number_of_boreholes = 65        # REQUIRED
    length_of_boreholes = 127.09    # REQUIRED

    # 2. Building inputs
    #####################################################
    building_file = 'GHP_scenario.xlsx'  # REQUIRED 
                                    # This file include timeseries of electric consumption, 
                                    # GHP size, floor area for each building

    # 3. Fuel prices (For BAU scenario and REopt format)
    #####################################################
    fuel_cost_per_mmbtu = 13.5


    # 4. Capital costs 
    # OPTIONAL, if not provided ('NA'), 
    # REopt default values will be used
    #####################################################
    installed_cost_heatpump_per_ton = 'NA'                  # GHP installation cost per ton
    installed_cost_ghx_per_ft = 'NA'                        # GHX installation cost per ft
    installed_cost_building_hydronic_loop_per_sqft = 'NA'   # Hydronic loop installation cost per sqft
    om_cost_per_sqft_year = 0                               # O&M cost

    # 5. Financials 
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
    
    return (lon,lat,buildings_id,number_of_boreholes,length_of_boreholes,building_file,fuel_cost_per_mmbtu,
            macrs_bonus_fraction,macrs_itc_reduction,federal_itc_fraction,utility_tarrif,om_cost_per_sqft_year,
            installed_cost_heatpump_per_ton,installed_cost_ghx_per_ft,installed_cost_building_hydronic_loop_per_sqft)

addInputs()                      