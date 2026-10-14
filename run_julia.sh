path="/Users/apham/Documents/Projects/REopt_Projects/FY27/GHP replacement cost/"
scenario_name="ghp_test"
isitBAU=0

python processInputs.py "$path" "$scenario_name" "$isitBAU"
julia runREopt.jl "$path" "$scenario_name"
python processOutputs.py "$path" "$scenario_name" "$isitBAU"
