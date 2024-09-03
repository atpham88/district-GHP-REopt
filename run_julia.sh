path="/Users/apham/Documents/Projects/REopt_Projects/FY24/Geothermal/Workshop/demo"
scenario_name="demo"

python processInputs.py "$path"
julia runREopt.jl "$path"
python processOutputs.py "$path" "$scenario_name"