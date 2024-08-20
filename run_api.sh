scenario_name="test"

python processInputs.py "$scenario_name"
python callREoptAPI.py "$scenario_name"
python processOutputs.py "$scenario_name"