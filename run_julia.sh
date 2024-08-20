scenario_name="test"

python processInputs.py "$scenario_name"
julia runREopt.jl "$scenario_name"
python processOutputs.py "$scenario_name"