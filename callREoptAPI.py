import json
import os
import site
#import src
from src.post_and_poll import get_api_results

API_KEY = 'cCeLsoUMlcwU8XhWLLhrxMV1SnSc9t2aBkdjbUjS'  # REPLACE WITH YOUR API KEY


##############################################################################################################
dir = os.getcwd()
inputs_path = os.path.join("data", 'inputs_all')
outputs_path = os.path.join("results", 'results_json')
##############################################################################################################

for item in os.listdir(inputs_path):
    if item == ".DS_Store":
        continue
    else:
        post_name = os.path.join(inputs_path, item)

    # Load post:
    with open(post_name, 'r') as fp:
        post = json.load(fp)
    
    results_file_name = post_name
    root_url = "http://0.0.0.0:8000/stable" # /stable == /v3 
    
    site.addsitedir("/home/jovyan/work/REopt API Scripts")
    #from src.post_and_poll import get_api_results
    api_response = get_api_results(post=post, 
                                   API_KEY=API_KEY, 
                                   api_url=root_url, 
                                   results_file=os.path.join(outputs_path, item ), 
                                   run_id=None)