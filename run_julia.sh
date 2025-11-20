path="/Users/apham/Documents/Projects/REopt_Projects/FY26/URBANopt-REopt/unbalanced vs balanced loads"
scenario_name="unbalanced"
isitBAU=0

python processInputs.py "$path" "$scenario_name" "$isitBAU"
julia runREopt.jl "$path" "$scenario_name"
python processOutputs.py "$path" "$scenario_name" "$isitBAU"