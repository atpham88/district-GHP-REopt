path="/Users/apham/Documents/Projects/REopt_Projects/FY25/URBANopt_REopt/5_building_site"
scenario_name="GHP_standalone"
isitBAU=0    

python processInputs.py "$path" "$scenario_name" "$isitBAU"
julia runREopt.jl "$path" "$scenario_name"
python processOutputs.py "$path" "$scenario_name" "$isitBAU"