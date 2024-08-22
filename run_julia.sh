path="/Users/apham/Documents/Projects/REopt_Projects/FY24/Geothermal/testing/GHP_investment"
scenario_name="GHP_investment"

python processInputs.py "$path"
julia runREopt.jl "$path"
python processOutputs.py "$path" "$scenario_name"