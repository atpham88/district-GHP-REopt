
def addInputs():
    ########################################################################################################## 
    # Specify all your building and district energy system inputs in this file #
    ##########################################################################################################
    
    # 1. District inputs
    ##########################################################################################################
    district_file = 'district.csv'  # REQUIRED 
                                    # This file includes GHX size (borehole #, length) and 
                                    # site location (lon, lat) 

    # 2. Building inputs
    ##########################################################################################################
    building_file = 'building.xlsx'  # REQUIRED 
                                     # This file includes timeseries of electric consumption, 
                                     # GHP size, floor area for each building

    # 3. Capital amd O&M costs 
    # OPTIONAL, if not provided ('NA'), REopt default values will be used
    ##########################################################################################################
    installed_cost_heatpump_per_ton = 1904                  # GHP installation cost per ton
    replacement_year = 10                                   # Replace GHP equipment after this number of years
    replace_cost_per_ton = 952                              # Cost of replace GHP equipment after replacement_year
    installed_cost_ghx_per_ft = 19                          # GHX installation cost per ft
    installed_cost_building_hydronic_loop_per_sqft = 0      # Hydronic loop installation cost per sqft
    om_cost_per_sqft_year = 0                               # O&M cost
    fuel_cost_per_mmbtu = 15                                # Fuel cost of the BAU/backup system
    installed_cost_per_mmbtu_per_hour = 56000               # Installed cost of new boiler (if GHP is not invested)

    # 4. Financials 
    # OPTIONAL, if not provided ('NA'), 
    # REopt default values will be used
    ##########################################################################################################
    macrs_bonus_fraction = 'NA'                    
    macrs_itc_reduction = 'NA'
    federal_itc_fraction = 'NA'
    offtaker_discount_rate_fraction = 'NA'
    offtaker_tax_rate_fraction = 'NA'
    om_cost_escalation_rate_fraction = 'NA'
    elec_cost_escalation_rate_fraction = 'NA'
    owner_discount_rate_fraction = 'NA'
    owner_tax_rate_fraction = 'NA'

    # 6. Utility Tariff
    # REQUIRED
    # Three options, flat rate (utility_rate), urdb label (string), monthly rates, or custom json file
    ##########################################################################################################
    utility_rate = 'custom'         # 'flat', 'label', 'monthly_rates', or 'custom'
    annual_energy_rate = 0.25       # Provide rate if utility_rate = 'flat'

    if utility_rate == 'label':
        utility_tarrif = "utility_label.csv"    # Provide if using urdb label ("utility_label.csv") 
    elif utility_rate == 'monthly_rates':
        utility_tarrif = "utility_rates.csv"    # if custom json file ("utility_rates.csv" )
    elif utility_rate == 'custom':
        utility_tarrif = "utility_rates.json"   # if custom json file ("utility_rates.json" )

    
    return (building_file,district_file,macrs_bonus_fraction,macrs_itc_reduction,federal_itc_fraction,
            offtaker_discount_rate_fraction,offtaker_tax_rate_fraction,om_cost_escalation_rate_fraction,
            elec_cost_escalation_rate_fraction,owner_discount_rate_fraction,owner_tax_rate_fraction,
            utility_tarrif,utility_rate,annual_energy_rate,utility_tarrif,om_cost_per_sqft_year,
            installed_cost_heatpump_per_ton,replacement_year,replace_cost_per_ton,
            installed_cost_ghx_per_ft,installed_cost_building_hydronic_loop_per_sqft,
            fuel_cost_per_mmbtu,installed_cost_per_mmbtu_per_hour)

addInputs()                      
