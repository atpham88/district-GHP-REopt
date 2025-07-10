path="/Users/apham/Documents/Projects/REopt_Projects/FY25/URBANopt_REopt/5_building_site"
scenario_name="no_fractions"

python processInputs.py "$path" "$scenario_name"
julia runREopt.jl "$path"
python processOutputs.py "$path" "$scenario_name"