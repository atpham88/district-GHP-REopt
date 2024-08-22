path="/Users/apham/Documents/Projects/REopt_Projects/FY24/Geothermal/testing/GHP_investment"
scenario_name="GHP_investment"

python processInputs.py "$scenario_name"
python callREoptAPI.py "$scenario_name"
python processOutputs.py "$scenario_name"