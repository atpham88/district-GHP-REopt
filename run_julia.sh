path="/Users/apham/Documents/Projects/REopt_Projects/FY24/Geothermal/DEC_module_testing/test"
scenario_name="test"

python processInputs.py "$path"
julia runREopt.jl "$path"
python processOutputs.py "$path" "$scenario_name"